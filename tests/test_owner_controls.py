from decimal import Decimal
import pytest
from landscaper.calculator import build_quote, load_pricing
from landscaper.owner_controls import OverrideBook, PriceRejected

P = load_pricing()


def test_override_applies_and_audited():
    book = OverrideBook(P)
    book.set_price("sod", "1.50", actor="owner")
    q = build_quote([("sod", 100)], P, book.prices)
    assert q.lines[0].unit_price == Decimal("1.50") and q.lines[0].overridden
    assert book.audit[0]["old"] == "1.20" and book.audit[0]["new"] == "1.50"


@pytest.mark.parametrize("price", ["0", "-1", "0.01", "50"])
def test_override_guard_rails(price):
    with pytest.raises(PriceRejected):
        OverrideBook(P).set_price("sod", price, actor="owner")
