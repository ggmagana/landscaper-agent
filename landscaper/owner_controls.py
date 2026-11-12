"""Owner price control with guard rails and an audit trail."""
from __future__ import annotations

import time
from decimal import Decimal

from .calculator import default_unit_price
from .money import D, money


class PriceRejected(ValueError):
    pass


class OverrideBook:
    """Holds the owner's price overrides. Every change is recorded."""

    def __init__(self, pricing: dict, low=Decimal("0.25"), high=Decimal("4")):
        self.pricing, self.low, self.high = pricing, low, high
        self.prices: dict[str, Decimal] = {}
        self.audit: list[dict] = []

    def set_price(self, service: str, price, actor: str) -> Decimal:
        if service not in self.pricing["services"]:
            raise PriceRejected(f"unknown service: {service}")
        p = money(price)
        base = default_unit_price(service, self.pricing)
        if p <= 0 or p < base * self.low or p > base * self.high:
            raise PriceRejected(
                f"{p} is outside the safe range for {service} "
                f"({money(base * self.low)} to {money(base * self.high)})")
        old = self.prices.get(service, base)
        self.prices[service] = p
        self.audit.append({"ts": time.time(), "actor": actor, "service": service,
                           "old": str(old), "new": str(p)})
        return p

    def clear(self, service: str, actor: str) -> None:
        if service in self.prices:
            old = self.prices.pop(service)
            self.audit.append({"ts": time.time(), "actor": actor, "service": service,
                               "old": str(old), "new": "default"})
