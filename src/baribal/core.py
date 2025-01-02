"""Core functionality for DataFrame inspection."""
from typing import Optional, Union, Any

import pandas as pd
import polars as pl


def _get_frame_info(df: Union[pd.DataFrame, pl.DataFrame]) -> tuple[int, int]:
    """Get the number of rows and columns for either pandas or polars DataFrame."""
    if isinstance(df, pd.DataFrame):
        return df.shape[0], df.shape[1]
    return df.shape[0], df.shape[1]


def _get_columns(df: Union[pd.DataFrame, pl.DataFrame]) -> list[str]:
    """Get column names for either pandas or polars DataFrame."""
    if isinstance(df, pd.DataFrame):
        return list(df.columns)
    return df.columns


def _get_dtype(df: Union[pd.DataFrame, pl.DataFrame], col: str) -> str:
    """Get dtype for a column in either pandas or polars DataFrame."""
    if isinstance(df, pd.DataFrame):
        return str(df[col].dtype)
    return str(df.schema[col])


def _get_sample_values(
    df: Union[pd.DataFrame, pl.DataFrame],
    col: str,
    n: int = 5
) -> list[Any]:
    """Get first n values from a column in either pandas or polars DataFrame."""
    if isinstance(df, pd.DataFrame):
        return df[col].head(n).tolist()
    return df.select(col).head(n)[col].to_list()


def _format_type(type_str: str) -> str:
    """Format type string to be consistent and readable.
    All types are normalized to 3 characters for alignment."""
    # Normalize type string format
    type_str = str(type_str).lower()
    if 'object' in type_str:
        return 'chr'
    if 'int' in type_str:
        return 'int'
    if 'float' in type_str:
        return 'num'
    if 'bool' in type_str:
        return 'log'  # 'log' for logical instead of 'lgl'
    if 'datetime' in type_str:
        return 'dtm'  # 'dtm' instead of 'dttm'
    if 'date' in type_str:
        return 'dte'  # 'dte' instead of 'date'
    if 'string' in type_str or 'str' in type_str:
        return 'chr'
    # Tronquer à 3 caractères pour tout autre type
    return type_str[:3].lower()


def glimpse(
    df: Union[pd.DataFrame, pl.DataFrame],
    width: Optional[int] = None,
    max_values: int = 5,
    max_value_width: int = 20,
) -> None:
    """Provide a glimpse of a DataFrame, inspired by R's glimpse function.
    Works with both pandas and polars DataFrames.

    Args:
        df: The DataFrame to inspect (pandas or polars)
        width: Maximum display width. If None, uses terminal width
        max_values: Maximum number of values to show per column
        max_value_width: Maximum width for displaying individual values
    """
    if not isinstance(df, (pd.DataFrame, pl.DataFrame)):
        raise TypeError("Input must be either a pandas DataFrame or a polars DataFrame")

    try:
        import shutil
        terminal_width = shutil.get_terminal_size().columns
    except Exception:
        terminal_width = 80

    width = width or terminal_width

    # Display dimensions
    n_rows, n_cols = _get_frame_info(df)
    print(f"Observations: {n_rows}")
    print(f"Variables: {n_cols}")

    # Find maximum column name length for alignment
    max_name_length = max((len(str(col)) for col in _get_columns(df)), default=0)

    # Helper function to format a single value
    def format_value(val) -> str:
        if val is None or (isinstance(val, float) and pd.isna(val)):
            return "NA"
        
        val_str = str(val)
        if isinstance(val, str):
            val_str = f'"{val}"'
        
        if len(val_str) > max_value_width:
            return val_str[:max_value_width-3] + "..."
        return val_str

    # Process and display each column
    for col in _get_columns(df):
        # Get column type
        col_type = _format_type(_get_dtype(df, col))
        
        # Get sample values
        sample_vals = _get_sample_values(df, col, max_values)
        formatted_vals = [format_value(val) for val in sample_vals]
        values_str = ", ".join(formatted_vals)

        # Format column name with right padding
        col_name = str(col).ljust(max_name_length)
        
        # Construct the column line with aligned type
        col_line = f"$ {col_name} <{col_type}> {values_str}"
        
        # Truncate if too long
        if len(col_line) > width:
            col_line = col_line[:width-3] + "..."
        
        print(col_line)