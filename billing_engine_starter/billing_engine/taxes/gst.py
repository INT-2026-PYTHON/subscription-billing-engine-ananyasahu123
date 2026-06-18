"""
GSTCalculator — Indian Goods & Services Tax.

The rule:
    - If customer_state == seller_state (or seller_state is "")  =>  intra-state
        -> charge CGST + SGST (split equally, e.g. 9% + 9% = 18%)
    - Else  =>  inter-state
        -> charge IGST (e.g. 18%)

Customers without a state code default to IGST (safe choice).
"""

from decimal import Decimal

from billing_engine.money import Money
from billing_engine.taxes.base import TaxCalculator, TaxContext, TaxBreakdown


class GSTCalculator(TaxCalculator):
    def __init__(self, cgst: Decimal, sgst: Decimal, igst: Decimal) -> None:
        # TODO Day 1
        #   - Validate each rate is Decimal in [0, 1].
        #   - Validate cgst + sgst == igst (sanity check on Indian GST setup).
        #   - Store on self.
        raise NotImplementedError("Day 1: implement GSTCalculator.__init__")

    def apply(self, taxable: Money, context: TaxContext) -> TaxBreakdown:
        # TODO Day 1
        #   - Decide intra vs inter-state from context.
        #     intra = bool(context.customer_state) and context.customer_state == context.seller_state
        #   - If intra: components = [("CGST X%", taxable*cgst), ("SGST Y%", taxable*sgst)], total = sum
        #   - Else:     components = [("IGST Z%", taxable*igst)],                            total = igst leg
        raise NotImplementedError("Day 1: implement GSTCalculator.apply")
class GSTCalculator(TaxCalculator):

    def __init__(self, cgst: Decimal, sgst: Decimal, igst: Decimal) -> None:
        for name, rate in [("cgst", cgst), ("sgst", sgst), ("igst", igst)]:
            if not (Decimal("0.00") <= rate <= Decimal("1.00")):
                raise ValueError(f"{name} rate must be between 0.00 and 1.00")
                
        if cgst + sgst != igst:
            raise ValueError(f"Invalid GST configuration: CGST ({cgst}) + SGST ({sgst}) must equal IGST ({igst})")
            
        self.cgst = cgst
        self.sgst = sgst
        self.igst = igst

    def apply(self, taxable: Money, context: TaxContext) -> TaxBreakdown:
        customer_state = getattr(context, "customer_state", getattr(context, "state_code", ""))
        seller_state = getattr(context, "seller_state", "")

        is_intra = bool(customer_state) and customer_state == seller_state

        if is_intra:
            cgst_amount = taxable * self.cgst
            sgst_amount = taxable * self.sgst
            total_tax = cgst_amount + sgst_amount
            
            components = [
                (f"CGST {self.cgst * 100}%", cgst_amount),
                (f"SGST {self.sgst * 100}%", sgst_amount)
            ]
            rate_summary = f"CGST {self.cgst * 100}% + SGST {self.sgst * 100}%"
        else:
            total_tax = taxable * self.igst
            components = [
                (f"IGST {self.igst * 100}%", total_tax)
            ]
            rate_summary = f"IGST {self.igst * 100}%"

        return TaxBreakdown(
            total=total_tax,
            components=components,
            rate_summary=rate_summary
        )