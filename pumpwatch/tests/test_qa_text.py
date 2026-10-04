"""QA: cashtag extraction, hype scoring and near-duplicate detection."""

from __future__ import annotations

import pytest

from pumpwatch.text import extract_cashtags, hype_score, jaccard, near_duplicate_clusters, shingles

ZW = "​"
CAMPAIGN = (
    "Huge news coming for $ABC this week get in now before it explodes "
    "target five dollars by friday"
)


# -- correct today: keep it that way -----------------------------------------
@pytest.mark.parametrize(
    "text, expected",
    [
        ("$5", ()),
        ("$1.2M raised", ()),
        ("paid $20 for it", ()),
        ("$TSLA's run", ("TSLA",)),
        ("$ABCDEF", ()),
        ("$$ABC", ()),
        ("buy $abc and $ABC now", ("ABC",)),
        ("קנו $ABC עכשיו", ("ABC",)),
        ("$ABC,$XYZ.", ("ABC", "XYZ")),
    ],
)
def test_cashtag_edge_cases_that_work(text, expected):
    assert extract_cashtags(text) == expected


def test_known_universe_filters_noise():
    assert extract_cashtags("$CEO says $ABC", known={"abc"}) == ("ABC",)


def test_hype_score_basics():
    assert hype_score("Quarterly results attached.") == 0.0
    assert hype_score("$ABC to the moon 🚀🚀🚀 get in now!!!") > 0.9
    assert hype_score("הזדמנות של פעם בחיים, להיכנס עכשיו") > 0.9
    assert 0.0 <= hype_score("🚀" * 50 + "!" * 50) <= 1.0


def test_identical_copy_paste_clusters_and_ticker_swap_is_ignored():
    items = [("a", CAMPAIGN), ("b", CAMPAIGN), ("c", CAMPAIGN.replace("$ABC", "$XYZ"))]
    assert near_duplicate_clusters(items) == [[0, 1, 2]]


def test_unrelated_messages_do_not_cluster():
    items = [
        ("a", "The quarterly report for ABC is out and revenue grew compared with last year"),
        ("b", "Anyone know when the annual meeting is scheduled, cannot find it on the site"),
        ("c", CAMPAIGN),
    ]
    assert near_duplicate_clusters(items) == []


# -- QA-6: format characters ----------------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-6")
@pytest.mark.parametrize("text", [f"to the m{ZW}oon", "to the moo­n", f"buy{ZW} now"])
def test_hype_score_ignores_invisible_characters(text):
    assert hype_score(text) == hype_score(text.replace(ZW, "").replace("­", ""))


@pytest.mark.xfail(strict=True, reason="QA-6")
def test_zero_width_spaces_do_not_break_near_duplicate_detection():
    poisoned = CAMPAIGN.replace("coming", f"com{ZW}ing").replace("explodes", f"expl{ZW}odes").replace(
        "dollars", f"dol{ZW}lars"
    )
    assert jaccard(shingles(CAMPAIGN), shingles(poisoned)) == 1.0


@pytest.mark.xfail(strict=True, reason="QA-6")
def test_zero_width_inside_cashtag_does_not_yield_wrong_ticker():
    assert extract_cashtags(f"$AB{ZW}CD") in (("ABCD",), ())


# -- QA-14: typographic apostrophes ----------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-14")
@pytest.mark.parametrize("text", ["Don’t miss this", "DON’T MISS"])
def test_smart_apostrophe_counts_as_hype(text):
    assert hype_score(text) >= 0.7


# -- QA-15: substring false positives ----------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-15")
@pytest.mark.parametrize(
    "text",
    ["download updates here", "vipers game tonight", "a 10x10 grid"],
)
def test_hype_phrases_match_whole_words_only(text):
    assert hype_score(text) == 0.0


@pytest.mark.xfail(strict=True, reason="QA-15")
def test_negated_guarantee_is_not_hype():
    assert hype_score("Returns are not guaranteed, do your own research") < 0.35


# -- QA-17: cashtag regex gaps ---------------------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-17")
@pytest.mark.parametrize(
    "text, expected",
    [
        ("ל$ABC", ("ABC",)),  # Hebrew prefix letter attached to the cashtag
        ("ו$ABC עולה", ("ABC",)),
        ("＄ABC", ("ABC",)),  # fullwidth dollar sign
        ("$ＡＢＣ", ("ABC",)),  # fullwidth letters
        ("$BRK.B", ("BRK.B",)),  # class shares
    ],
)
def test_cashtag_regex_gaps(text, expected):
    assert extract_cashtags(text) == expected


# -- QA-20: paraphrase sensitivity -------------------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-20")
def test_one_word_paraphrase_still_counts_as_near_duplicate():
    """Changing a single word of an 18-word pitch must not escape S5."""

    para = CAMPAIGN.replace("before", "prior to")
    items = [("a", CAMPAIGN), ("b", para), ("c", CAMPAIGN.replace("week", "month"))]
    assert near_duplicate_clusters(items) == [[0, 1, 2]]
