from decimal import Decimal
from landscaper.money import fmt, money


def test_money_rounds_half_up_and_never_float_drift():
    assert money("2.665") == Decimal("2.67")
    assert fmt(1234.5) == "$1,234.50"
