# tests/test_amort.py

import pytest
from loan_amort.amort import amortize_loan

def test_zero_interest():
    # a 1-year $1,000 loan paid quarterly at 0% interest
    schedule = amortize_loan(1000.0, 0.0, 1, payments_per_year=4)
    assert len(schedule) == 4
    for p in schedule:
        # all interest payments should be zero
        assert p["interest"] == 0.0
        # principal should be exactly 250 each period
        assert p["principal"] == pytest.approx(250.0)
        # payment = principal + interest
        assert p["payment"] == pytest.approx(250.0)

def test_standard_loan_principal_sum():
    # a 1-year $100 loan at 10% annual, monthly
    schedule = amortize_loan(100.0, 0.10, 1, payments_per_year=12)
    total_principal = sum(p["principal"] for p in schedule)
    # should fully amortize the $100 principal
    assert total_principal == pytest.approx(100.0, rel=1e-6)

