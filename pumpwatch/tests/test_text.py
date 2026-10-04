from pumpwatch.text import extract_cashtags, hype_score, jaccard, near_duplicate_clusters, shingles


def test_cashtags_basic_and_dedup():
    assert extract_cashtags("buy $abc and $ABC and $xyz now") == ("ABC", "XYZ")


def test_cashtags_ignore_money_amounts():
    assert extract_cashtags("raised $5 million at $1.2M valuation") == ()


def test_cashtags_possessive_and_punctuation():
    assert extract_cashtags("$TSLA's run, ($GME)!") == ("TSLA", "GME")


def test_cashtags_universe_filter():
    assert extract_cashtags("$ABC $USD", known={"ABC"}) == ("ABC",)


def test_cashtags_inside_hebrew_text():
    assert extract_cashtags("המניה $ABCD תטוס היום") == ("ABCD",)


def test_hype_scores_promotion_above_ordinary_talk():
    promo = hype_score("$ABC is about to explode!!! get in now 🚀🚀 100x guaranteed")
    calm = hype_score("$ABC reported results, revenue up slightly, margins thin")
    assert promo > 0.9
    assert calm < 0.2


def test_hype_score_bounded():
    s = hype_score("🚀" * 50 + "!" * 50 + " guaranteed 100x to the moon buy now")
    assert 0.0 <= s <= 1.0


def test_hebrew_hype():
    assert hype_score("המניה הזו תטוס, להיכנס עכשיו, פי 10") > 0.9


def test_near_duplicates_cluster_and_ignore_cashtag_swaps():
    items = [
        ("a", "$AAA is about to explode, huge news coming, get in now"),
        ("b", "$BBB is about to explode, huge news coming, get in now"),
        ("c", "$CCC is about to explode, huge news coming, get in now!!"),
        ("d", "quarterly results were fine, nothing special here"),
    ]
    clusters = near_duplicate_clusters(items, threshold=0.6)
    assert clusters == [[0, 1, 2]] or sorted(map(sorted, clusters)) == [[0, 1, 2]]


def test_jaccard_edges():
    assert jaccard(frozenset(), frozenset({"a"})) == 0.0
    s = shingles("one two three four five")
    assert jaccard(s, s) == 1.0
