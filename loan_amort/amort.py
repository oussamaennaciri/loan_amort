# loan_amort/amort.py

import datetime
from typing import List, Dict, Any
from dateutil.relativedelta import relativedelta

def amortize_loan(
    principal: float,
    annual_rate: float,
    years: int,
    payments_per_year: int = 12,
    first_payment_date: datetime.date = None
) -> List[Dict[str, Any]]:
    """
    Generate an amortization schedule, optionally with payment dates.

    Args:
        principal: initial loan amount
        annual_rate: annual interest rate (decimal, e.g. 0.05)
        years: term of loan in years
        payments_per_year: payments per year (default 12)
        first_payment_date: date of the first payment (datetime.date), or None

    Returns:
        List of payment records with keys:
          period, payment, interest, principal, balance[, date]
    """
    # periodic rate and total periods
    r = annual_rate / payments_per_year
    n = years * payments_per_year

    # fixed payment formula
    if r == 0:
        payment = principal / n
    else:
        payment = principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

    # build dates list if requested
    if first_payment_date:
        months_between = 12 // payments_per_year
        dates = [
            first_payment_date + relativedelta(months=months_between * (i - 1))
            for i in range(1, n + 1)
        ]
    else:
        dates = [None] * n

    balance = principal
    schedule: List[Dict[str, Any]] = []

    for period in range(1, n + 1):
        interest = balance * r
        principal_paid = payment - interest

        # on last payment, absorb rounding error
        if period == n:
            principal_paid = balance
            payment = interest + principal_paid

        balance -= principal_paid

        row: Dict[str, Any] = {
            "period": period,
            "payment": round(payment, 2),
            "interest": round(interest, 2),
            "principal": round(principal_paid, 2),
            "balance": round(max(balance, 0), 2),
        }
        if dates[period - 1]:
            row["date"] = dates[period - 1].isoformat()

        schedule.append(row)

    return schedule

