"""Tests for rename_all function."""
import pandas as pd
import polars as pl
import pytest

from baribal.utils import rename_all


@pytest.fixture
def sample_df():
    """Create sample DataFrame for testing."""
    return pd.DataFrame({
        'Col_1': [1, 2, 3],
        'Col_2': [4, 5, 6],
        'Special@Column': [7, 8, 9],
        'Mixed_CASE_name': [10, 11, 12]
    })


def test_rename_with_case(sample_df):
    """Test renaming with case conversion."""
    result = rename_all(sample_df, r'Col_(\d+)', case='lower')
    result_columns = list(result.columns)
    print("Result columns:", result_columns)  # Pour le debug
    # On s'attend à ce que chaque colonne du résultat soit en minuscules
    assert all(name == name.lower() for name in result_columns)


def test_rename_regex(sample_df):
    """Test renaming with regex pattern."""
    result = rename_all(sample_df, r'Col_(\d+)')
    assert all(name in result.columns for name in ['1', '2'])
    assert 'Special@Column' in result.columns


def test_rename_case_options(sample_df):
    """Test different case conversion options."""
    # Test lower
    result = rename_all(sample_df, lambda x: x, case='lower')
    expected_lower = ['col_1', 'col_2', 'special@column', 'mixed_case_name']
    assert result.columns.tolist() == expected_lower

    # Test upper
    result = rename_all(sample_df, lambda x: x, case='upper')
    expected_upper = ['COL_1', 'COL_2', 'SPECIAL@COLUMN', 'MIXED_CASE_NAME']
    assert result.columns.tolist() == expected_upper

    # Test title
    result = rename_all(sample_df, lambda x: x, case='title')
    # Pour title case, accepter soit Col_1 soit Col_1 pour les nombres
    for col in result.columns:
        if '_' in col:
            words = col.split('_')
            for word in words:
                # Ignorer les parties numériques
                if not word.isdigit():
                    assert word[0].isupper() and word[1:].islower(), \
                        f"Word {word} in column {col} is not properly title cased"


def test_rename_polars():
    """Test with Polars DataFrame."""
    df = pl.DataFrame({
        'Col_1': [1, 2, 3],
        'Col_2': [4, 5, 6]
    })
    # Sans case spécifié, on garde juste les nombres
    result = rename_all(df, r'Col_(\d+)')
    assert all(name in result.columns for name in ['1', '2'])
    
    # Avec case spécifié, on ajoute le préfixe approprié
    result = rename_all(df, r'(Col_\d+)', case='lower')
    assert all(name in result.columns for name in ['col_1', 'col_2'])
