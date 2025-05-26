import pandas as pd
from loan_amort.amort import amortize_loan

EXPECTED_COLUMNS = {
    "period",
    "date",
    "beginning_balance",
    "payment",
    "interest",
    "principal",
    "ending_balance",
}

def test_amortize_loan_basic_schedule():
    term = 12
    df = amortize_loan(
        principal=1000.0,
        annual_rate=0.05,
        term_months=term,
        start_date="2025-06-01"
    )

    # It should be a DataFrame
    assert isinstance(df, pd.DataFrame)

    # It must have exactly the expected columns
    assert set(df.columns) == EXPECTED_COLUMNS

    # It should have one row per month in the term
    assert len(df) == term
