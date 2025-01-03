"""Core functionality for DataFrame inspection."""
from typing import Any, Optional, Union

import numpy as np
import pandas as pd
import polars as pl
from scipy import stats


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

    All types are normalized to 3 characters for alignment.
    """
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


def _calculate_percentages(
    df: pd.DataFrame,
    margin_normalize: Optional[str] = None
) -> pd.DataFrame:
    """Calculate percentages for the contingency table."""
    if margin_normalize == 'index':
        return df.div(df.sum(axis=1), axis=0) * 100
    elif margin_normalize == 'columns':
        return df.div(df.sum(axis=0), axis=1) * 100
    else:
        total = df.sum().sum()
        return (df / total) * 100


def _calculate_statistics(
    contingency_table: pd.DataFrame
) -> dict:
    """Calculate chi-square and related statistics."""
    # Préparation de la table
    # Retirer la ligne et colonne 'All' si elles existent
    if 'All' in contingency_table.index:
        table = contingency_table.drop('All')
    else:
        table = contingency_table

    if 'All' in table.columns:
        table = table.drop('All', axis=1)

    # Vérifier si la table est valide pour le calcul
    if (table.empty or
        table.sum().sum() == 0 or
        table.shape[0] < 2 or
        table.shape[1] < 2):
        return {
            'chi2': 0.0,
            'p_value': 1.0,
            'cramer_v': 0.0
        }

    try:
        # Retirer les lignes/colonnes avec que des zéros
        mask_rows = table.sum(axis=1) > 0
        mask_cols = table.sum(axis=0) > 0
        table = table.loc[mask_rows, mask_cols]

        if table.shape[0] < 2 or table.shape[1] < 2:
            return {
                'chi2': 0.0,
                'p_value': 1.0,
                'cramer_v': 0.0
            }

        # Calculer chi2 et V de Cramer
        chi2, p_value, dof, expected = stats.chi2_contingency(table)
        n = table.sum().sum()
        min_dim = min(table.shape) - 1

        # Gestion explicite des cas limites
        if chi2 < 0 or n <= 0 or min_dim <= 0:
            cramer_v = 0.0
        else:
            try:
                cramer_v = float(np.sqrt(chi2 / (n * min_dim)))
                if np.isnan(cramer_v):
                    cramer_v = 0.0
            except (ValueError, ZeroDivisionError):
                cramer_v = 0.0

        return {
            'chi2': float(chi2) if not np.isnan(chi2) else 0.0,
            'p_value': float(p_value) if not np.isnan(p_value) else 1.0,
            'cramer_v': float(cramer_v) if not np.isnan(cramer_v) else 0.0
        }

    except Exception as e:
        print(f"Error in _calculate_statistics: {str(e)}")
        return {
            'chi2': 0.0,
            'p_value': 1.0,
            'cramer_v': 0.0
        }



def glimpse(
    df: Union[pd.DataFrame, pl.DataFrame],
    width: Optional[int] = None,
    max_values: int = 5,
    max_value_width: int = 20,
) -> None:
    """Provide a glimpse of a DataFrame, inspired by R's glimpse function."""
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
    print(f"DataFrame type: {'pandas' if isinstance(df, pd.DataFrame) else 'polars'}")

    # Find maximum column name length for alignment
    max_name_length = max((len(str(col)) for col in _get_columns(df)), default=0)

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

        # Construct the column line with aligned type (using <> instead of ())
        col_line = f"$ {col_name} <{col_type}> {values_str}"

        # Truncate if too long
        if len(col_line) > width:
            col_line = col_line[:width-3] + "..."

        print(col_line)


def tabyl(
    df: Union[pd.DataFrame, pl.DataFrame],
    *vars: str,
    show_na: bool = True,
    show_pct: bool = True,
    margin: bool = True,
) -> tuple[pd.DataFrame, Optional[dict]]:
    """Create enhanced cross-tabulations with integrated statistics."""
    if not isinstance(df, (pd.DataFrame, pl.DataFrame)):
        raise TypeError("Input must be either a pandas DataFrame or a polars DataFrame")

    # Convert to pandas if needed
    if isinstance(df, pl.DataFrame):
        try:
            df = df.to_pandas()
        except ModuleNotFoundError as err:
            raise ImportError("pyarrow is required for converting polars to pandas") \
                from err


    if not vars:
        raise ValueError("At least one variable must be specified")

    # Validate all variables exist in DataFrame
    missing_vars = [var for var in vars if var not in df.columns]
    if missing_vars:
        raise ValueError(f"Variables not found in DataFrame: {missing_vars}")

    # Handle NA values
    df_copy = df.copy()
    if not show_na:
        df_copy = df_copy.dropna(subset=list(vars))

    # Create cross-tabulation
    if len(vars) == 1:
        # Single variable frequency table
        result = pd.DataFrame(df_copy[vars[0]].value_counts(dropna=not show_na))
        if show_pct:
            result['percentage'] = result / len(df_copy) * 100
        stats_dict = None

    elif len(vars) == 2:
        # Two-way cross-tabulation
        result = pd.crosstab(
            df_copy[vars[0]],
            df_copy[vars[1]],
            margins=margin,
            dropna=not show_na
        )

        if show_pct:
            pct_row = _calculate_percentages(result, 'index')
            pct_col = _calculate_percentages(result, 'columns')
            pct_total = _calculate_percentages(result)

            result = pd.concat([
                result,
                pct_row.add_suffix('_pct_row'),
                pct_col.add_suffix('_pct_col'),
                pct_total.add_suffix('_pct_total')
            ], axis=1)

        # Calculate statistics (excluding margins)
        if result.size > 0:  # Check if table is not empty
            if margin:
                stats_table = result.iloc[:-1, :-1]
            else:
                stats_table = result

            try:
                stats_dict = _calculate_statistics(stats_table)
            except ValueError:
                stats_dict = None
        else:
            stats_dict = None

    else:
        # Multi-way cross-tabulation
        result = pd.crosstab(
            [df_copy[var] for var in vars[:-1]],
            df_copy[vars[-1]],
            margins=margin,
            dropna=not show_na
        )

        if show_pct:
            result = pd.concat([
                result,
                _calculate_percentages(result, 'index').add_suffix('_pct_row')
            ], axis=1)

        stats_dict = None

    return result, stats_dict
