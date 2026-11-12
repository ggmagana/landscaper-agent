from landscaper.calculator import build_quote, load_pricing
from landscaper.explain import explain_quote
from landscaper.i18n import t

P = load_pricing()


def test_explanations_cover_every_line_in_both_languages():
    q = build_quote([("sod", 1000), ("mulch", 4)], P, {"mulch": "70"})
    for lang in ("en", "es"):
        txt = explain_quote(q, P, lang)
        assert txt.count("•") == 2
        assert "Total" in txt
    assert "dueño" in explain_quote(q, P, "es")
    assert "owner set" in explain_quote(q, P, "en")
    assert t("ack", "fr") == t("ack", "en")
