# Utils API Reference

This module provides utility functions for DataFrame column manipulation and cleaning.

## Functions

### `clean_names`

```python
def clean_names(
    df: Union[pd.DataFrame, pl.DataFrame],
    case: str = "snake",
    remove_special: bool = True,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
    max_length: Optional[int] = None,
) -> Union[pd.DataFrame, pl.DataFrame]
```

Clean column names to make them easier to handle, inspired by the janitor package in R.

#### Parameters

- `df`: DataFrame to clean column names for
- `case`: Case style (default: "snake")
  - 'snake': convert to snake_case
  - 'camel': convert to camelCase
  - 'pascal': convert to PascalCase
  - 'upper': convert to UPPER_CASE
  - 'lower': convert to lower_case
- `remove_special`: Whether to remove special characters and accents (default: True)
- `prefix`: Prefix to add to all column names (default: None)
- `suffix`: Suffix to add to all column names (default: None)
- `max_length`: Maximum length for column names (default: None)

#### Returns

DataFrame with cleaned column names

#### Examples

Basic usage:
```python
import pandas as pd
import baribal as bb

df = pd.DataFrame({
    "First Name": [1, 2, 3],
    "Last.Name": [4, 5, 6],
    "Age!": [7, 8, 9]
})

# Convert to snake_case
clean_df = bb.clean_names(df)
print(clean_df.columns)
# Output: ['first_name', 'last_name', 'age']

# Convert to PascalCase
clean_df = bb.clean_names(df, case='pascal')
print(clean_df.columns)
# Output: ['FirstName', 'LastName', 'Age']
```

With prefix and suffix:
```python
clean_df = bb.clean_names(df, prefix='col_', suffix='_var')
print(clean_df.columns)
# Output: ['col_first_name_var', 'col_last_name_var', 'col_age_var']
```

### `rename_all`

```python
def rename_all(
    df: Union[pd.DataFrame, pl.DataFrame],
    pattern: Union[str, dict[str, str], Callable[[str], str]],
    *,
    case: Optional[str] = None,
    remove_special: bool = False,
) -> Union[pd.DataFrame, pl.DataFrame]
```

Rename all columns in a DataFrame according to a pattern, inspired by the rename_all function from dplyr.

#### Parameters

- `df`: Input DataFrame (pandas or polars)
- `pattern`: Pattern for renaming columns. Can be:
  - str: Regular expression pattern with a capture group
  - dict: Mapping of old names to new names
  - Callable: Function that takes old name and returns new name
- `case`: Optional case transformation ('lower', 'upper', 'title')
- `remove_special`: Whether to remove special characters (default: False)

#### Returns

DataFrame with renamed columns

#### Examples

Using regex pattern:
```python
import pandas as pd
import baribal as bb

df = pd.DataFrame({
    'Col_1': [1, 2, 3],
    'Col_2': [4, 5, 6]
})

# Keep only the numbers from column names
result = bb.rename_all(df, r'Col_(\d+)')
print(result.columns)
# Output: ['1', '2']

# Convert to lowercase after applying pattern
result = bb.rename_all(df, r'(Col_\d+)', case='lower')
print(result.columns)
# Output: ['col_1', 'col_2']
```

Using dictionary:
```python
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [4, 5, 6]
})

# Rename using dictionary
result = bb.rename_all(df, {'a': 'col_a', 'b': 'col_b'})
print(result.columns)
# Output: ['col_a', 'col_b']
```

Using function:
```python
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [4, 5, 6]
})

# Rename using function
result = bb.rename_all(df, lambda x: f'col_{x.upper()}')
print(result.columns)
# Output: ['col_A', 'col_B']
```