# Usage Guide

## Getting Started

Baribal brings R-inspired data manipulation functions to Python's pandas ecosystem. Here's how to get started:

```python
import pandas as pd
import baribal as bb

# Create a sample DataFrame
df = pd.DataFrame({
    'First Name': ['Alice', 'Bob', 'Charlie'],
    'Last.Name': ['Smith', 'Jones', 'Brown'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
})
```

## Key Features

### Quick Data Overview with `glimpse()`

The `glimpse()` function provides a concise summary of your DataFrame:

```python
bb.glimpse(df)
```

Output:
```
Observations: 3
Variables: 4
DataFrame type: pandas
$ First Name <chr> "Alice", "Bob", "Charlie"
$ Last.Name  <chr> "Smith", "Jones", "Brown"
$ Age        <int> 25, 30, 35
$ City       <chr> "New York", "London", "Paris"
```

### Cleaning Column Names

Clean up messy column names with `clean_names()`:

```python
clean_df = bb.clean_names(df)
print(clean_df.columns)
# Output: ['first_name', 'last_name', 'age', 'city']

# Using different case styles
pascal_df = bb.clean_names(df, case='pascal')
print(pascal_df.columns)
# Output: ['FirstName', 'LastName', 'Age', 'City']
```

### Advanced Cross-tabulations

Create enhanced frequency tables and cross-tabulations with `tabyl()`:

```python
# Simple frequency table
result, _ = bb.tabyl(df, 'city')
print(result)

# Cross-tabulation with statistics
result, stats = bb.tabyl(df, 'city', 'age')
print("\nCross-tabulation:")
print(result)
print("\nStatistics:")
print(stats)
```

### Column Renaming Patterns

Apply consistent renaming patterns with `rename_all()`:

```python
# Using regex pattern
df_renamed = bb.rename_all(df, r'(.*) Name', case='lower')

# Using a function
df_renamed = bb.rename_all(df, lambda x: f"col_{x.lower()}")
```

## Working with Missing Data

Baribal includes features for handling missing data:

```python
# Get summary of missing values
missing_df = bb.missing_summary(df)
print(missing_df)
```

## Tips and Best Practices

1. **Column Naming Conventions**
   - Use `clean_names()` early in your data pipeline
   - Choose a consistent case style for your project
   - Consider adding prefixes for specific data types

2. **Performance Considerations**
   - `glimpse()` is optimized for large DataFrames
   - Use `tabyl()` with `show_na=False` to exclude missing values
   - Set appropriate `max_length` in `clean_names()` for very long column names

3. **Working with Both pandas and polars**
   - All functions support both pandas and polars DataFrames
   - Consistent API across both libraries
   - Output maintains the same type as input

## Common Patterns

### Data Cleaning Pipeline

```python
def clean_data(df):
    """Example data cleaning pipeline using Baribal."""
    # Clean column names
    df = bb.clean_names(df, case='snake')
    
    # Analyze missing values
    missing = bb.missing_summary(df)
    print("Missing values summary:")
    print(missing)
    
    # Get overview of cleaned data
    bb.glimpse(df)
    
    return df
```

### Statistical Analysis

```python
def analyze_categorical(df, var1, var2):
    """Example categorical analysis using Baribal."""
    # Create cross-tabulation
    result