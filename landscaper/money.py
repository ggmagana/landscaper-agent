from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")


def D(x) -> Decimal:
    """Convert to Decimal via str so 0.1 stays 0.1 (never use float for money)."""
    return x if isinstance(x, Decimal) else Decimal(str(x))


def money(x) -> Decimal:
    return D(x).quantize(CENT, rounding='ROUND_HALF_UP')


def fmt(x) -> str:
    return f"${money(x):,.2f}"
