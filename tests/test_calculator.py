from decimal import Decimal
import pytest
from landscaper.calculator import build_quote, default_unit_price, load_pricing

P = load_pricing()


def test_default_price_sod():
    # (0.55 + 0.010*45) * 1.20 = 1.20
    assert default_unit_price("sod", P) == Decimal("1.20")


def test_quote_totals():
    q = build_quote([("sod", 1000)], P)
    assert q.subtotal == Decimal("1200.00")
    assert q.tax == Decimal("99.00")
    assert q.total == Decimal("1299.00")


def test_minimum_charge():
    q = build_quote([("sprinkler_repair", 0.1)], P)
    assert q.minimum_applied and q.subtotal == Decimal("75.00")


@pytest.mark.parametrize("bad", [0, -5, 10**9])
def test_bad_quantity(bad):
    with pytest.raises(ValueError):
        build_quote([("sod", bad)], P)


def test_unknown_service():
    with pytest.raises(ValueError):
        build_quote([("moon_base", 1)], P)
