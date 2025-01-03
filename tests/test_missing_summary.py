"""Tests for the glimpse function."""
import pandas as pd

from baribal.viz import missing_summary


# Correctly calculates missing value statistics for pandas DataFrame input
def test_calculates_missing_stats_for_pandas_df():
    # Create test DataFrame with known missing values
    df = pd.DataFrame({
        'col1': [1, None, 3, None, 5],
        'col2': [1, 1, None, 4, 4]
    })

    result = missing_summary(df)

    # Verify missing counts
    assert result.loc['col1', 'missing_count'] == 2
    assert result.loc['col2', 'missing_count'] == 1

    # Verify missing percentages
    assert result.loc['col1', 'missing_percentage'] == 40.0
    assert result.loc['col2', 'missing_percentage'] == 20.0

    # Verify unique counts
    assert result.loc['col1', 'unique_count'] == 3
    assert result.loc['col2', 'unique_count'] == 2


# Handles empty DataFrame input
def test_handles_empty_dataframe():
    # Create empty DataFrame
    df = pd.DataFrame()

    result = missing_summary(df)

    # Verify empty DataFrame is returned
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
    assert list(result.columns) == ['missing_count', 'missing_percentage', 'value_counts', 'unique_count']