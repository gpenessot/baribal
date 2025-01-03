"""Tests for clean_names function."""
import pandas as pd
import polars as pl
import pytest

from baribal.utils import clean_names


@pytest.fixture
def messy_df():
    """Create DataFrame with messy column names."""
    return pd.DataFrame({
        "First Name": [1],
        "Last.Name": [2],
        "Age!": [3],
        "Email@Address": [4],
        "Phone #": [5],
        "2nd_Address": [6],
        "Création_été": [7],
        " Trailing Space ": [8],
        "Multiple__Underscores": [9]
    })


def test_clean_names_basic(messy_df):
    """Test basic cleaning with default parameters."""
    result = clean_names(messy_df)
    
    assert all(name.islower() for name in result.columns)
    assert all('_' not in name[0] for name in result.columns)
    assert all(name.isascii() for name in result.columns)
    assert all(' ' not in name for name in result.columns)
    assert all('.' not in name for name in result.columns)


def test_clean_names_case_styles(messy_df):
    """Test different case styles."""
    # Snake case (default)
    result = clean_names(messy_df)
    assert 'first_name' in result.columns
    
    # Camel case
    result = clean_names(messy_df, case='camel')
    assert 'firstName' in result.columns
    
    # Pascal case
    result = clean_names(messy_df, case='pascal')
    assert 'FirstName' in result.columns
    
    # Upper case
    result = clean_names(messy_df, case='upper')
    assert 'FIRST_NAME' in result.columns


def test_clean_names_prefix_suffix(messy_df):
    """Test prefix and suffix options."""
    result = clean_names(messy_df, prefix='col_', suffix='_var')
    assert all(name.startswith('col_') for name in result.columns)
    assert all(name.endswith('_var') for name in result.columns)


def test_clean_names_max_length(messy_df):
    """Test maximum length constraint."""
    result = clean_names(messy_df, max_length=10)
    assert all(len(name) <= 10 for name in result.columns)


def test_clean_names_polars():
    """Test with Polars DataFrame."""
    df = pl.DataFrame({
        "First Name": [1],
        "Last.Name": [2],
        "Age!": [3]
    })
    result = clean_names(df)
    assert isinstance(result, pl.DataFrame)
    assert 'first_name' in result.columns


def test_clean_names_special_chars(messy_df):
    """Test handling of special characters and accents."""
    # With special chars removal
    result = clean_names(messy_df, remove_special=True)
    print(result.columns)
    assert 'creation_ete' in result.columns
    
    # Without special chars removal
    result = clean_names(messy_df, remove_special=False)
    print(result.columns)
    assert any('é' in name for name in result.columns)


def test_clean_names_numeric_start():
    """Test handling of column names starting with numbers."""
    df = pd.DataFrame({
        "1st_column": [1],
        "2nd_column": [2]
    })
    result = clean_names(df)
    assert all(not name[0].isdigit() for name in result.columns)
