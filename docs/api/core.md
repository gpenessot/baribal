# Core API Reference

This module provides the core functionality for DataFrame inspection and analysis.

## Functions

### `glimpse`

```python
def glimpse(
    df: Union[pd.DataFrame, pl.DataFrame],
    width: Optional[int] = None,
    max_values: int = 5,
    max_value_width: int = 20,
) -> None
```

Provide a glimpse of a DataFrame, inspired by R's glimpse function. This function gives a concise summary of your DataFrame's structure and content.

#### Parameters

- `df`: Input DataFrame (pandas or polars)
- `width`: Maximum width of the output (defaults to terminal width)
- `max_values`: Maximum number of sample values to show per column (default: 5)
- `max_value_width`: Maximum width for displaying individual values (default: 20)

#### Returns

None (prints to stdout)

#### Examples

```python
import pandas as pd
import baribal as bb

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['New York', 'London', 'Paris']
})

bb.glimpse(df)
```

Output:
```
Observations: 3
Variables: 3
DataFrame type: pandas
$ name <chr> "Alice", "Bob", "Charlie"
$ age  <int> 25, 30, 35
$ city <chr> "New York", "London", "Paris"
```

### `tabyl`

```python
def tabyl(
    df: Union[pd.DataFrame, pl.DataFrame],
    *vars: str,
    show_na: bool = True,
    show_pct: bool = True,
    margin: bool = True,
) -> tuple[pd.DataFrame, Optional[dict]]
```

Create enhanced cross-tabulations with integrated statistics, inspired by the janitor package in R.

#### Parameters

- `df`: Input DataFrame (pandas or polars)
- `*vars`: One or more column names to tabulate
- `show_na`: Include NA values in the tabulation (default: True)
- `show_pct`: Include percentage calculations (default: True)
- `margin`: Include row and column totals (default: True)

#### Returns

A tuple containing:
1. DataFrame: The cross-tabulation results
2. Optional[dict]: Statistical measures for two-way tables (chi-square test results and Cramer's V)
   - Only provided for two-way tables
   - Contains 'chi2', 'p_value', and 'cramer_v' keys

#### Examples

Single variable frequency table:
```python
import pandas as pd
import baribal as bb

df = pd.DataFrame({
    'category': ['A', 'B', 'A', 'B', 'A'],
    'status': ['Active', 'Active', 'Inactive', 'Active', 'Active']
})

result, _ = bb.tabyl(df, 'category')
print(result)
```

Two-way cross-tabulation with statistics:
```python
result, stats = bb.tabyl(df, 'category', 'status')
print("Cross-tabulation:")
print(result)
print("\nStatistics:")
print(stats)
```

Three-way cross-tabulation:
```python
result, _ = bb.tabyl(df, 'category', 'status', 'region')
print(result)
```

#### Notes

- For two-way tables, statistical measures include:
  - Chi-square test of independence
  - P-value for the chi-square test
  - Cramer's V measure of association
- Percentages can be calculated for:
  - Row totals (_pct_row suffix)
  - Column totals (_pct_col suffix)
  - Overall totals (_pct_total suffix)