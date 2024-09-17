from __future__ import annotations

import numpy_financial as npf


class MortgageCalculator:
    def __init__(self, principal: float, interest_rate: float, term: int):
        self.principal = principal
        self.interest_rate = interest_rate
        self.term = (
            term * 12
        )  # Assuming 'term' was initially in years, converting it to months.

    def calculate_monthly_payment_interest_only(self) -> float:
        """Calculates the monthly payment for an interest-only mortgage."""
        return round(self.principal * (self.interest_rate / 12), 2)

    def calculate_monthly_payment_repayment(self) -> float:
        """Calculates the monthly payment for a repayment mortgage using numpy-financial."""
        monthly_rate = self.interest_rate / 12
        payment = npf.pmt(monthly_rate, self.term, -self.principal)
        return round(payment, 2)

    def calculate_total_repayment(self) -> float:
        """Calculates the total amount to be repaid over the life of the mortgage."""
        monthly_payment = self.calculate_monthly_payment_repayment()
        return round(monthly_payment * self.term, 2)
