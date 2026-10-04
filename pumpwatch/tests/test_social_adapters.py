"""Offline tests for the social-data adapters. All fixtures are synthetic."""

from __future__ import annotations

import io
import json
from datetime import date
from pathlib import Path

import pytest

from pumpwatch.adapters import hash_author
from pumpwatch.adapters.posts_csv import load_posts_csv, read_posts_csv
from pumpwatch.adapters.telegram_export import (
    ExportStats,
    flatten_text,
    load_telegram_export,
    parse_telegram_export,
)
from pumpwatch.config import Config
from pumpwatch.context import TickerContext
from pumpwatch.signals.social import coordinated_promotion

FIX = Path(__file__).parent / "fixtures"
SALT = "test-salt-not-secret"


def ctx_for(ticker, posts):
    return TickerContext(ticker, [], [], [p for p in posts if ticker in p.tickers], {}, [])


# -- author hashing -----------------------------------------------------------


def test_hash_author_is_stable_salted_and_namespaced():
    a = hash_author("user2001", SALT, "telegram")
    assert a == hash_author("user2001", SALT, "telegram")
    assert a != hash_author("user2001", "other-salt", "telegram")
    assert a != hash_author("user2001", SALT, "reddit")
    assert a.startswith("telegram:") and "2001" not in a
    assert len(a.split(":", 1)[1]) == 16


def test_hash_author_requires_salt():
    with pytest.raises(ValueError):
        hash_author("user2001", "", "telegram")
    with pytest.raises(ValueError):
        hash_author("user2001", b"", "telegram")


# -- Telegram export ----------------------------------------------------------


def test_flatten_text_handles_strings_and_entity_lists():
    assert flatten_text("plain") == "plain"
    assert flatten_text(["a ", {"type": "cashtag", "text": "$ZZZQ"}, " b"]) == "a $ZZZQ b"
    assert flatten_text(None) == ""


def test_public_channel_export():
    stats = ExportStats()
    posts = load_telegram_export(FIX / "telegram_public_channel.json", SALT, stats=stats)
    assert len(posts) == 3
    assert stats.skipped_service == 1
    assert stats.skipped_empty == 1
    assert stats.skipped_untagged == 1
    assert {p.source for p in posts} == {"telegram"}

    first = posts[0]
    # date_unixtime (UTC) wins over the exporter's local "date".
    assert first.day == date(2026, 3, 2)
    assert first.tickers == ("ZZZQ",)
    assert "about to explode" in first.text

    assert posts[1].tickers == ("ZZZQ", "ABCD")
    # Hebrew text split into entities is flattened in order.
    assert posts[2].text == "פי 10 על $ZZZQ — להיכנס עכשיו"


def test_channel_posts_share_one_opaque_author():
    posts = load_telegram_export(FIX / "telegram_public_channel.json", SALT)
    authors = {p.author for p in posts}
    assert authors == {hash_author("channel9000000001", SALT, "telegram")}
    raw = (FIX / "telegram_public_channel.json").read_text(encoding="utf-8")
    for p in posts:
        assert p.author not in raw
        assert "Synthetic Promo Channel" not in p.author


def test_known_universe_filters_cashtags():
    posts = load_telegram_export(FIX / "telegram_public_channel.json", SALT, known=["zzzq"])
    assert [p.tickers for p in posts] == [("ZZZQ",)] * 3


def test_keep_untagged():
    posts = load_telegram_export(FIX / "telegram_public_channel.json", SALT, keep_untagged=True)
    assert len(posts) == 4
    assert any(p.tickers == () for p in posts)


def test_private_channel_is_refused():
    with pytest.raises(ValueError, match="private_channel"):
        load_telegram_export(FIX / "telegram_private_channel.json", SALT)


def test_account_export_reads_only_public_chats():
    stats = ExportStats()
    posts = load_telegram_export(FIX / "telegram_account_export.json", SALT, stats=stats)
    assert stats.chats_read == 1
    assert sorted(stats.chats_skipped_private) == ["personal_chat", "private_supergroup"]
    assert len(posts) == 4
    assert all("private note" not in p.text and "buy now" not in p.text for p in posts)
    assert len({p.author for p in posts}) == 3


def test_account_export_feeds_s5_coordinated_promotion():
    posts = load_telegram_export(FIX / "telegram_account_export.json", SALT)
    hit = coordinated_promotion(ctx_for("ZZZQ", posts), date(2026, 3, 4), Config())
    assert hit is not None
    assert "3 different accounts" in hit.evidence


def test_rejects_non_export_json():
    with pytest.raises(ValueError):
        parse_telegram_export({"hello": "world"}, SALT)
    with pytest.raises(ValueError):
        parse_telegram_export([], SALT)  # type: ignore[arg-type]


def test_bad_dates_are_skipped_not_fatal():
    data = {
        "type": "public_channel",
        "id": 1,
        "messages": [
            {"type": "message", "date": "not a date", "text": "$ZZZQ x"},
            {"type": "message", "date": "2026-03-04T10:00:00", "text": "$ZZZQ y"},
        ],
    }
    stats = ExportStats()
    posts = parse_telegram_export(json.loads(json.dumps(data)), SALT, stats=stats)
    assert [p.day for p in posts] == [date(2026, 3, 4)]
    assert stats.skipped_bad_date == 1


# -- generic CSV --------------------------------------------------------------


def test_posts_csv():
    posts = load_posts_csv(FIX / "posts.csv", SALT)
    assert len(posts) == 5
    assert posts[0].source == "reddit"
    assert posts[0].tickers == ("ZZZQ",)
    assert posts[1].day == date(2026, 3, 4)  # timestamp cut to its date
    assert posts[2].tickers == ("ZZZQ",)  # lower-case cashtag normalised
    # explicit tickers column wins, for sources without $cashtags
    assert posts[4].tickers == ("ZZZQ", "600000")
    # same raw author on the same source -> same opaque id
    assert posts[0].author == posts[3].author == hash_author("t2_fixture_alpha", SALT, "reddit")
    assert all("fixture" not in p.author for p in posts)


def test_posts_csv_known_filter_applies_to_explicit_tickers():
    posts = load_posts_csv(FIX / "posts.csv", SALT, known=["ZZZQ"])
    assert all(p.tickers == ("ZZZQ",) for p in posts)
    assert len(posts) == 4


def test_posts_csv_feeds_s5_across_sources():
    posts = load_posts_csv(FIX / "posts.csv", SALT)
    hit = coordinated_promotion(ctx_for("ZZZQ", posts), date(2026, 3, 5), Config())
    assert hit is not None
    assert "reddit, stocktwits, x" in hit.evidence


def test_posts_csv_missing_column():
    with pytest.raises(ValueError, match="day"):
        read_posts_csv(io.StringIO("source,author,text\nx,a,$ZZZQ\n"), SALT)


def test_posts_csv_bad_day_names_the_line():
    bad = "source,author,day,text\nx,a,2026-03-04,$ZZZQ ok\nx,a,04/03/2026,$ZZZQ\n"
    with pytest.raises(ValueError, match="line 3"):
        read_posts_csv(io.StringIO(bad), SALT)


def test_posts_csv_requires_author():
    with pytest.raises(ValueError, match="author"):
        read_posts_csv(io.StringIO("source,author,day,text\nx,,2026-03-04,$ZZZQ\n"), SALT)
