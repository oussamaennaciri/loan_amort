import pandas as pd
from datetime import datetime
from typing import Optional, Dict

def amortize_loan(
    principal: float,
    annual_rate: float,
    term_months: int,
    start_date: str,  # format "YYYY-MM-DD"
    loan_type: str = "amortizing",  # "amortizing" | "bullet" | "interest-only"
    extra_payments: Optional[Dict[str, float]] = None
) -> pd.DataFrame:
    """
    Generate an amortization schedule.

    Returns a DataFrame with columns:
      period, date, beginning_balance,
      payment, interest, principal, ending_balance
    """
    # Parse the first payment date
    first_date = datetime.strptime(start_date, "%Y-%m-%d")
    
    # Monthly rate and payment calculation
    r = annual_rate / 12.0
    n = term_months

    # Determine payment amount
    if loan_type == "amortizing":
        payment = (r * principal) / (1 - (1 + r) ** -n)
    elif loan_type in {"bullet", "interest-only"}:
        payment = principal * r
    else:
        raise ValueError(f"Unsupported loan_type: {loan_type}")

    records = []
    balance = principal

    # Generate payment dates
    dates = pd.date_range(start=first_date, periods=n, freq="MS")

    for i, pay_date in enumerate(dates, start=1):
        interest = balance * r

        if loan_type == "amortizing":
            principal_paid = payment - interest
        elif loan_type == "interest-only":
            principal_paid = 0.0 if i < n else principal
        elif loan_type == "bullet":
            principal_paid = 0.0 if i < n else principal

        extra = 0.0
        if extra_payments and pay_date.strftime("%Y-%m-%d") in extra_payments:
            extra = extra_payments[pay_date.strftime("%Y-%m-%d")]
            principal_paid += extra

        ending_balance = balance - principal_paid

        records.append({
            "period": i,
            "date": pay_date,
            "beginning_balance": balance,
            "payment": payment + (extra if loan_type == "amortizing" else 0.0),
            "interest": interest,
            "principal": principal_paid,
            "ending_balance": ending_balance,
        })

        balance = ending_balance

    df = pd.DataFrame.from_records(records)
    df["date"] = pd.to_datetime(df["date"])
    return df
