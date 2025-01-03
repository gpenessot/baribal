"""Demonstration of baribal's tabyl function capabilities.

This script shows various ways to use the tabyl function for data analysis,
from basic frequency tables to complex cross-tabulations with statistics.
"""
import pandas as pd
import polars as pl

from baribal import tabyl

# Create sample dataset
def create_sample_data():
    """Create a sample dataset for demonstration."""
    return pd.DataFrame({
        'department': ['Sales', 'IT', 'Marketing', 'Sales', 'IT', 'Marketing',
                      'Sales', 'IT', 'Marketing', 'Sales', 'IT', 'Marketing'],
        'status': ['Active', 'Active', 'Inactive', 'Active', 'Inactive', 'Active',
                  'Active', 'Active', 'Active', 'Inactive', 'Active', 'Active'],
        'experience': ['Junior', 'Senior', 'Senior', 'Junior', 'Senior', 'Junior',
                      'Senior', 'Senior', 'Junior', 'Senior', 'Junior', 'Senior'],
        'satisfaction': ['High', 'High', 'Medium', 'Low', 'High', 'High',
                        'Medium', 'High', 'High', 'Low', 'High', 'Medium']
    })

def main():
    """Run demo."""
    # Create our sample dataset
    df = create_sample_data()
    print("Sample Dataset:")
    print(df.head(), "\n")

    # 1. Single variable frequency table
    print("1. Basic frequency table for department:")
    result, _ = tabyl(df, 'department')
    print(result, "\n")

    # 2. Two-way cross-tabulation with statistics
    print("2. Department by Status with statistics:")
    result, stats = tabyl(df, 'department', 'status')
    print("Cross-tabulation:")
    print(result)
    print("\nStatistics:")
    print(f"Chi-square: {stats['chi2']:.2f}")
    print(f"P-value: {stats['p_value']:.4f}")
    print(f"Cramer's V: {stats['cramer_v']:.4f}\n")

    # 3. Three-way cross-tabulation
    print("3. Three-way cross-tabulation (Department × Status × Experience):")
    result, _ = tabyl(df, 'department', 'status', 'experience')
    print(result, "\n")

    # 4. Using without percentages
    print("4. Basic counts without percentages:")
    result, _ = tabyl(df, 'department', show_pct=False)
    print(result, "\n")

    # 5. Excluding NA values
    print("5. Frequency table excluding NA values:")
    df_with_na = df.copy()
    df_with_na.loc[0, 'department'] = None
    result, _ = tabyl(df_with_na, 'department', show_na=False)
    print(result, "\n")

    # 6. Analysis without margins
    print("6. Cross-tabulation without margins:")
    result, stats = tabyl(df, 'department', 'status', margin=False)
    print(result, "\n")

    # 7. Using with polars DataFrame
    print("7. Using tabyl with polars:")
    pl_df = pl.from_pandas(df)
    result, _ = tabyl(pl_df, 'department')
    print(result, "\n")

    # 8. Complex analysis example
    print("8. Complex analysis: Experience level impact on satisfaction by department:")
    result, stats = tabyl(df, 'experience', 'satisfaction')
    print("Cross-tabulation of experience and satisfaction:")
    print(result)
    if stats:
        print("\nAssociation statistics:")
        print(f"Chi-square: {stats['chi2']:.2f}")
        print(f"P-value: {stats['p_value']:.4f}")
        print(f"Cramer's V: {stats['cramer_v']:.4f}")

if __name__ == "__main__":
    main()
