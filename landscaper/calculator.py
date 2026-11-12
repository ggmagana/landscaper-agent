"""Deterministic quote math. The LLM never does arithmetic; this file does."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

from .money import D, money

DEFAULT_PRICING = Path(__file__).resolve().parent.parent / "data" / "pricing.json"


def load_pricing(path: Path | str = DEFAULT_PRICING) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


@dataclass(frozen=True)
class LineItem:
    service: str
    quantity: Decimal
    unit: str
    unit_price: Decimal      # what the customer pays per unit
    total: Decimal
    overridden: bool = False
    material: Decimal = Decimal("0")   # cost per unit (info for explanation)
    labor_hours: Decimal = Decimal("0")


@dataclass(frozen=True)
class Quote:
    lines: list
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    minimum_applied: bool = False
    labor_rate: Decimal = Decimal("0")
    markup: Decimal = Decimal("0")
    tax_rate: Decimal = Decimal("0")
    notes: list = field(default_factory=list)


def default_unit_price(service: str, pricing: dict) -> Decimal:
    s = pricing["services"][service]
    cost = D(s["material"]) + D(s["labor_hours"]) * D(pricing["labor_rate"])
    return money(cost * (1 + D(pricing["markup"])))


def build_quote(items: list[tuple[str, object]], pricing: dict,
                overrides: dict[str, object] | None = None) -> Quote:
    """items: [(service, quantity)]. overrides: {service: final unit price}."""
    overrides = overrides or {}
    if not items:
        raise ValueError("no items")
    lines = []
    for service, qty in items:
        if service not in pricing["services"]:
            raise ValueError(f"unknown service: {service}")
        q = D(qty)
        if q <= 0 or q > D(pricing["max_quantity"]):
            raise ValueError(f"bad quantity for {service}: {q}")
        s = pricing["services"][service]
        if service in overrides:
            up, over = money(overrides[service]), True
        else:
            up, over = default_unit_price(service, pricing), False
        lines.append(LineItem(service, q, s["unit"], up, money(up * q), over,
                              D(s["material"]), D(s["labor_hours"])))
    subtotal = sum((l.total for l in lines), Decimal("0"))
    minimum = False
    if subtotal < D(pricing["min_charge"]):
        subtotal, minimum = money(pricing["min_charge"]), True
    tax = money(subtotal * D(pricing["tax_rate"]))
    return Quote(lines, subtotal, tax, subtotal + tax, minimum,
                 D(pricing["labor_rate"]), D(pricing["markup"]), D(pricing["tax_rate"]))
