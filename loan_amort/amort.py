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

    Parameters
    ----------
    principal : float
        Initial loan amount.
    annual_rate : float
        Annual interest rate (e.g. 0.06 for 6%).
    term_months : int
        Total number of monthly payments.
    start_date : str
        Date of the first payment, "YYYY-MM-DD".
    loan_type : str
        One of "amortizing", "bullet", or "interest-only".
    extra_payments : dict, optional
        Mapping of payment-date (YYYY-MM-DD) to extra principal amount.

    Returns
    -------
    pd.DataFrame
        Columns: ['period', 'date', 'beginning_balance',
                  'payment', 'interest', 'principal', 'ending_balance']
    """
    # Parse the start date
    first_date = datetime.strptime(start_date, "%Y-%m-%d")
    
    # Placeholder: empty schedule
    columns = [
        "period", "date", "beginning_balance",
        "payment", "interest", "principal", "ending_balance"
    ]
    schedule = pd.DataFrame(columns=columns)

    # TODO: implement:
    #   • Compute fixed payment for amortizing loans
    #   • Build a pd.date_range of payment dates (monthly)
    #   • Loop through each period, calculate interest & principal
    #   • Handle bullet and interest-only cases
    #   • Apply extra_payments on matching dates
    #   • Populate the DataFrame rows

    return schedule

