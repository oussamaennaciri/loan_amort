import pytest
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

def test_amortize_loan_returns_empty_dataframe_with_expected_columns():
    df = amortize_loan(
        principal=1000.0,
        annual_rate=0.05,
        term_months=12,
        start_date="2025-06-01"
    )

    # Should be a DataFrame
    assert isinstance(df, pd.DataFrame)

    # Must have exactly the expected columns
    assert set(df.columns) == EXPECTED_COLUMNS

    # Stub returns empty
    assert df.empty

