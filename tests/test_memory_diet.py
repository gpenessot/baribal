"""Tests for memory_diet function."""
import pandas as pd
import numpy as np
import pytest

from baribal.utils import memory_diet


@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'id': range(1000),  # int64 par défaut
        'small_int': np.random.randint(0, 100, 1000),  # Peut être uint8
        'large_int': np.random.randint(-1000000, 1000000, 1000),  # Nécessite int32
        'float_col': np.random.randn(1000),  # float64 par défaut
        'category': np.random.choice(['A', 'B', 'C'], 1000),  # object par défaut
        'text': ['Text' + str(i % 100) for i in range(1000)]  # object avec cardinalité moyenne
    })


def test_numeric_downcasting(sample_df):
    """Test numeric type downcasting."""
    result = memory_diet(sample_df)
    
    # Vérifier que small_int est converti en uint8
    assert result['small_int'].dtype == np.uint8
    
    # Vérifier que large_int est converti en int32
    assert result['large_int'].dtype == np.int32
    
    # Vérifier que les valeurs sont préservées
    pd.testing.assert_series_equal(
        sample_df['small_int'].astype(np.uint8),
        result['small_int']
    )


def test_aggressive_mode(sample_df):
    """Test aggressive mode for categorical conversion."""
    result = memory_diet(sample_df, aggressive=True)
    
    # Vérifier que les colonnes catégorielles sont converties
    assert pd.api.types.is_categorical_dtype(result['category'])
    assert pd.api.types.is_categorical_dtype(result['text'])
    
    # Vérifier que les valeurs sont préservées
    assert set(sample_df['category'].unique()) == \
           set(result['category'].unique())


def test_memory_reduction(sample_df):
    """Test that memory usage is actually reduced."""
    result = memory_diet(sample_df)
    
    original_memory = sample_df.memory_usage(deep=True).sum()
    optimized_memory = result.memory_usage(deep=True).sum()
    
    assert optimized_memory < original_memory


def test_index_optimization(sample_df):
    """Test index optimization."""
    # Créer un index non optimal
    df_with_index = sample_df.set_index('id')
    result = memory_diet(df_with_index)
    
    # Vérifier que l'index est optimisé
    assert isinstance(result.index, pd.RangeIndex)


def test_float_downcasting(sample_df):
    """Test float downcasting."""
    result = memory_diet(sample_df)
    
    # Vérifier que les float64 sont convertis en float32 quand possible
    assert result['float_col'].dtype == np.float32


def test_invalid_input():
    """Test with invalid input type."""
    with pytest.raises(TypeError, match="Input must be a pandas DataFrame"):
        memory_diet([1, 2, 3])


def test_no_modification_of_original(sample_df):
    """Test that the original DataFrame is not modified."""
    original_dtypes = sample_df.dtypes.copy()
    _ = memory_diet(sample_df)
    
    pd.testing.assert_series_equal(original_dtypes, sample_df.dtypes)


def test_negative_integers(sample_df):
    """Test handling of negative integers."""
    # Ajouter une colonne avec des nombres négatifs petits
    df = sample_df.copy()
    df['small_neg'] = np.random.randint(-50, 50, 1000)
    
    result = memory_diet(df)
    
    # Vérifier que le type est int8 puisque la plage est petite
    assert result['small_neg'].dtype == np.int8
    
    # Vérifier que les valeurs sont préservées
    pd.testing.assert_series_equal(
        df['small_neg'].astype(np.int8),
        result['small_neg']
    )
