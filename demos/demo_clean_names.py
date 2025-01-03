"""Demonstration of baribal's clean_names function capabilities.

This script shows various ways to use the clean_names function for standardizing
column names in both pandas and polars DataFrames.
"""
from pathlib import Path

import pandas as pd
import polars as pl

from baribal import clean_names


def load_sample_data(use_polars: bool = False) -> pd.DataFrame:
    """Load the sample dataset."""
    data_path = Path(__file__).parent / "data" / "sample_data.csv"
    if use_polars:
        return pl.read_csv(data_path)
    return pd.DataFrame(pd.read_csv(data_path))

def demonstrate_basic_cleaning():
    """Demonstrate basic column cleaning with default parameters."""
    print("\n1. Basic column cleaning (default snake_case):")
    df = load_sample_data()
    print("\nOriginal column names:")
    print(df.columns.tolist())

    cleaned_df = clean_names(df)
    print("\nCleaned column names (default snake_case):")
    print(cleaned_df.columns.tolist())

def demonstrate_case_styles():
    """Demonstrate different case style options."""
    df = load_sample_data()

    print("\n2. Different case styles:")

    # Camel case
    camel_df = clean_names(df, case='camel')
    print("\nCamel case:")
    print(camel_df.columns.tolist())

    # Pascal case
    pascal_df = clean_names(df, case='pascal')
    print("\nPascal case:")
    print(pascal_df.columns.tolist())

    # Upper case
    upper_df = clean_names(df, case='upper')
    print("\nUpper case:")
    print(upper_df.columns.tolist())

def demonstrate_special_characters():
    """Demonstrate handling of special characters and accents."""
    df = load_sample_data()

    print("\n3. Special character handling:")

    # Keep special characters
    print("\nWith special characters preserved:")
    preserved_df = clean_names(df, remove_special=False)
    print(preserved_df.columns.tolist())

    # Remove special characters
    print("\nWith special characters removed:")
    removed_df = clean_names(df, remove_special=True)
    print(removed_df.columns.tolist())

def demonstrate_prefix_suffix():
    """Demonstrate prefix and suffix options."""
    df = load_sample_data()

    print("\n4. Using prefix and suffix:")
    modified_df = clean_names(df, prefix='col_', suffix='_var')
    print(modified_df.columns.tolist())

def demonstrate_max_length():
    """Demonstrate maximum length constraint."""
    df = load_sample_data()

    print("\n5. Maximum length constraint:")
    truncated_df = clean_names(df, max_length=10)
    print(truncated_df.columns.tolist())

def demonstrate_polars_support():
    """Demonstrate support for polars DataFrame."""
    df = load_sample_data(use_polars=True)

    print("\n6. Polars support:")
    print("\nOriginal polars DataFrame columns:")
    print(df.columns)

    cleaned_df = clean_names(df)
    print("\nCleaned polars DataFrame columns:")
    print(cleaned_df.columns)

def main():
    """Run all demonstrations."""
    print("CLEAN_NAMES FUNCTION DEMONSTRATION")
    print("=================================")

    demonstrate_basic_cleaning()
    demonstrate_case_styles()
    demonstrate_special_characters()
    demonstrate_prefix_suffix()
    demonstrate_max_length()
    demonstrate_polars_support()

if __name__ == "__main__":
    main()
