"""Tests for the glimpse function."""
import pandas as pd
import polars as pl
import pytest

from baribal.core import glimpse


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    data = {
        "a": [1, 2, 3],
        "b": ["x", "y", "z"]
    }
    return data


def test_glimpse_pandas(sample_data, capsys):
    """Test glimpse with a pandas DataFrame."""
    df = pd.DataFrame(sample_data)
    
    glimpse(df)
    captured = capsys.readouterr()
    output = captured.out.strip().split("\n")
    
    assert "Rows: 3" in output[0]
    assert "Columns: 2" in output[1]
    assert "DataFrame type: pandas" in output[2]
    assert "$ a (int64) 1, 2, 3" in output[3]
    assert '$ b (object) "x", "y", "z"' in output[4]


def test_glimpse_polars(sample_data, capsys):
    """Test glimpse with a polars DataFrame."""
    df = pl.DataFrame(sample_data)
    
    glimpse(df)
    captured = capsys.readouterr()
    output = captured.out.strip().split("\n")
    
    assert "Rows: 3" in output[0]
    assert "Columns: 2" in output[1]
    assert "DataFrame type: polars" in output[2]
    assert "$ a (Int64) 1, 2, 3" in output[3]
    assert '$ b (String) "x", "y", "z"' in output[4]


def test_glimpse_long_values_pandas(capsys):
    """Test glimpse with long string values in pandas."""
    df = pd.DataFrame({
        "text": ["This is a very long string that should be truncated" * 3]
    })
    
    glimpse(df, width=50)
    captured = capsys.readouterr()
    assert len(captured.out.strip().split("\n")[3]) <= 50


def test_glimpse_long_values_polars(capsys):
    """Test glimpse with long string values in polars."""
    df = pl.DataFrame({
        "text": ["This is a very long string that should be truncated" * 3]
    })
    
    glimpse(df, width=50)
    captured = capsys.readouterr()
    assert len(captured.out.strip().split("\n")[3]) <= 50


def test_glimpse_missing_values_pandas(capsys):
    """Test glimpse with missing values in pandas."""
    df = pd.DataFrame({
        "with_na": [1, None, 3, pd.NA, 5]
    })
    
    glimpse(df)
    captured = capsys.readouterr()
    assert "NA" in captured.out


def test_glimpse_missing_values_polars(capsys):
    """Test glimpse with missing values in polars."""
    df = pl.DataFrame({
        "with_na": [1, None, 3, None, 5]
    })
    
    glimpse(df)
    captured = capsys.readouterr()
    assert "NA" in captured.out


def test_glimpse_invalid_input():
    """Test glimpse with invalid input."""
    with pytest.raises(TypeError, match="Input must be either a pandas DataFrame or a polars DataFrame"):
        glimpse([1, 2, 3])  # List instead of DataFrame


def test_glimpse_empty_pandas(capsys):
    """Test glimpse with an empty pandas DataFrame."""
    df = pd.DataFrame()
    
    glimpse(df)
    captured = capsys.readouterr()
    output = captured.out.strip().split("\n")
    
    assert "Rows: 0" in output[0]
    assert "Columns: 0" in output[1]


def test_glimpse_empty_polars(capsys):
    """Test glimpse with an empty polars DataFrame."""
    df = pl.DataFrame()
    
    glimpse(df)
    captured = capsys.readouterr()
    output = captured.out.strip().split("\n")
    
    assert "Rows: 0" in output[0]
    assert "Columns: 0" in output[1]