"""Core functionality for DataFrame inspection and analysis."""
from typing import Optional, Union, Any, Dict

import pandas as pd
import polars as pl
import numpy as np


def missing_summary(
    df: Union[pd.DataFrame, pl.DataFrame],
    threshold: float = 0.0,
) -> pd.DataFrame:
    """Generate a comprehensive summary of missing values in the DataFrame.
    
    Args:
        df: Input DataFrame (pandas or polars)
        threshold: Minimum proportion of missing values to include in report (0.0 to 1.0)
    
    Returns:
        DataFrame containing missing value statistics for each column:
        - missing_count: Number of missing values
        - missing_percentage: Percentage of missing values
        - value_counts: Distribution of top 3 most common values
        - unique_count: Number of unique non-missing values
    """
    # Convert Polars to Pandas if necessary
    if isinstance(df, pl.DataFrame):
        df = df.to_pandas()
    
    total_rows = len(df)
    
    # Initialize results dictionary
    results = {
        'missing_count': [],
        'missing_percentage': [],
        'value_counts': [],
        'unique_count': []
    }
    
    for column in df.columns:
        # Count missing values
        missing_count = df[column].isna().sum()
        missing_percentage = (missing_count / total_rows) * 100
        
        # Only include if meets threshold
        if missing_percentage >= threshold * 100:
            results['missing_count'].append(missing_count)
            results['missing_percentage'].append(round(missing_percentage, 2))
            
            # Get value distribution (top 3 most common values)
            value_counts = df[column].value_counts().head(3)
            formatted_counts = ', '.join(
                f"{v}: {c}" for v, c in value_counts.items()
            )
            results['value_counts'].append(formatted_counts)
            
            # Count unique values (excluding NA)
            unique_count = df[column].nunique(dropna=True)
            results['unique_count'].append(unique_count)
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(results, index=df.columns)
    
    # Sort by missing percentage descending
    summary_df = summary_df.sort_values('missing_percentage', ascending=False)
    
    return summary_df