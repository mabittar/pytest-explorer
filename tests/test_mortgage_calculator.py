from __future__ import annotations

from src.core import MortgageCalculator


def test_calculate_monthly_payment_interest_only():
    mortgage = MortgageCalculator(100000, 0.03, 30)
    assert mortgage.calculate_monthly_payment_interest_only() == 250.0


def test_calculate_monthly_payment_repayment():
    mortgage = MortgageCalculator(100000, 0.03, 30)
    assert mortgage.calculate_monthly_payment_repayment() == 421.60


def test_calculate_total_repayment():
    mortgage = MortgageCalculator(100000, 0.03, 30)
    assert mortgage.calculate_total_repayment() == 151776.0
