import pytest
import pandas as pd
from loan_amort.amort import amortize_loan

EXPECTED_COLUMNS = [
    "period",
    "date",
    "beginning_balance",
    "payment",
    "interest",
    "principal",
    "ending_balance"
]

def test_amortize_loan_returns_dataframe_with_correct_columns():
    # Call the stub function
    df = amortize_loan(
        principal=1000.0,
        annual_rate=0.05,
        term_months=12,
        start_date="2025-06-01"
    )

    # It should be a pandas DataFrame
    assert isinstance(df, pd.DataFrame), "Expected a pandas DataFrame"

    # It should have the right columns (order doesn’t matter)
    assert set(df.columns) == set(EXPECTED_COLUMNS), \
        f"DataFrame columns {df.columns.tolist()} do not match expected {EXPECTED_COLUMNS}"

    # Since the implementation is a stub, it should be empty
    assert df.shape[0] == 0, "Expected an empty DataFrame for the stub implementation"

