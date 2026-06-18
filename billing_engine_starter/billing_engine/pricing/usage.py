"""
UsageBased — pay per unit consumed.

Example: ₹0.50 per API call. Customer makes 1200 calls => charge = ₹600.
"""

from billing_engine.money import Money
from billing_engine.pricing.base import PricingStrategy

class UsageBased(PricingStrategy):

    def __init__(self, unit_price: Money) -> None:
        self.unit_price = unit_price

    def calculate(self, quantity: int) -> Money:
        if quantity <= 0:
            return Money(0, self.unit_price.currency)
        return self.unit_price * quantity