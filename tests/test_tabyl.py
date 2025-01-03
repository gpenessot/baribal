"""Tests for tabyl function."""
import pytest
import pandas as pd
import polars as pl
import numpy as np
from baribal.core import tabyl


@pytest.fixture
def simple_data():
    """Create a simple dataset for basic testing."""
    return pd.DataFrame({
        'category': ['A', 'B', 'A', 'B', 'A', None],
        'status': ['Active', 'Active', 'Inactive', 'Active', 'Active', 'Active'],
    })


@pytest.fixture
def complex_data():
    """Create a more complex dataset for testing edge cases."""
    return pd.DataFrame({
        'category': ['A', 'B', 'A', 'B', 'A', None, 'C', 'C'],
        'status': ['Active', 'Active', 'Inactive', 'Active', 'Active', 'Active', None, 'Inactive'],
        'region': ['North', 'South', 'North', 'South', 'North', 'South', 'North', 'South'],
        'value': [1, 2, 3, 4, 5, 6, 7, 8]
    })


def test_single_var_basic(simple_data):
    """Test basic single variable frequency table."""
    result, stats = tabyl(simple_data, 'category')
    
    assert isinstance(result, pd.DataFrame)
    assert result.index.tolist() == ['A', 'B', None]
    assert result.iloc[0, 0] == 3  # Count for 'A'
    assert 'percentage' in result.columns
    assert stats is None


def test_two_vars_basic(simple_data):
    """Test basic two-way cross-tabulation."""
    result, stats = tabyl(simple_data, 'category', 'status')
    
    assert isinstance(result, pd.DataFrame)
    assert isinstance(stats, dict)
    assert all(key in stats for key in ['chi2', 'p_value', 'cramer_v'])
    assert result.columns.str.contains('_pct_row').any()
    assert result.columns.str.contains('_pct_col').any()


def test_three_vars(complex_data):
    """Test three-way cross-tabulation."""
    result, stats = tabyl(complex_data, 'category', 'status', 'region')
    
    assert isinstance(result, pd.DataFrame)
    assert result.index.nlevels == 2  # Multi-index
    assert stats is None  # No stats for 3+ way tables
    assert result.columns.str.contains('_pct_row').any()


def test_no_na(simple_data):
    """Test excluding NA values."""
    result, _ = tabyl(simple_data, 'category', show_na=False)
    
    assert None not in result.index
    assert not result.index.isnull().any()


def test_no_percentages(simple_data):
    """Test without percentage calculations."""
    result, _ = tabyl(simple_data, 'category', show_pct=False)
    
    assert 'percentage' not in result.columns
    assert not result.columns.str.contains('_pct').any()


def test_no_margins(simple_data):
    """Test without margins in two-way table."""
    result, _ = tabyl(simple_data, 'category', 'status', margin=False)
    
    assert 'All' not in result.index
    assert 'All' not in result.columns


def test_polars_input():
    """Test with Polars DataFrame input."""
    pl_df = pl.DataFrame({
        'category': ['A', 'B', 'A'],
        'status': ['X', 'Y', 'X']
    })
    
    result, _ = tabyl(pl_df, 'category')
    assert isinstance(result, pd.DataFrame)


def test_invalid_inputs(simple_data):
    """Test various invalid inputs."""
    # No variables specified
    with pytest.raises(ValueError, match="At least one variable must be specified"):
        tabyl(simple_data)
    
    # Non-existent variable
    with pytest.raises(ValueError, match="Variables not found in DataFrame"):
        tabyl(simple_data, 'nonexistent')
    
    # Invalid DataFrame type
    with pytest.raises(TypeError):
        tabyl([1, 2, 3], 'category')


def test_all_na_column(complex_data):
    """Test handling of columns with all NA values."""
    complex_data['all_na'] = None
    result, _ = tabyl(complex_data, 'all_na', 'status')
    
    assert result is not None
    assert not result.empty


def test_statistical_measures(simple_data):
    """Test the statistical measures for two-way tables."""
    result, stats = tabyl(simple_data, 'category', 'status')
    
    # Afficher la table de contingence pour le débogage
    print("\nTable de contingence:")
    print(result)
    print("\nStatistiques:")
    print(stats)
    
    # Vérifier les types
    assert isinstance(stats['cramer_v'], float), f"Type invalide pour cramer_v: {type(stats['cramer_v'])}"
    assert isinstance(stats['p_value'], float), f"Type invalide pour p_value: {type(stats['p_value'])}"
    assert isinstance(stats['chi2'], float), f"Type invalide pour chi2: {type(stats['chi2'])}"
    
    # Vérifier que les valeurs sont dans les intervalles attendus
    assert not np.isnan(stats['cramer_v']), "Cramer's V should not be NaN"
    assert 0 <= stats['cramer_v'] <= 1, f"Cramer's V should be between 0 and 1, got {stats['cramer_v']}"
    assert 0 <= stats['p_value'] <= 1, f"p-value should be between 0 and 1, got {stats['p_value']}"
    assert stats['chi2'] >= 0, f"chi-square should be non-negative, got {stats['chi2']}"
    
    # Test avec des données qui devraient donner une mesure d'association faible
    df_indep = pd.DataFrame({
        'A': ['X', 'X', 'Y', 'Y'] * 25,
        'B': ['M', 'N', 'M', 'N'] * 25
    })
    _, indep_stats = tabyl(df_indep, 'A', 'B')
    assert indep_stats['cramer_v'] < 0.1  # Proche de 0 pour des variables indépendantes
