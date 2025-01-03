"""Utility functions for DataFrame column manipulation."""
import re
import unicodedata
from typing import Callable, Optional, Union, dict

import pandas as pd
import polars as pl


def clean_names(
    df: Union[pd.DataFrame, pl.DataFrame],
    case: str = "snake",
    remove_special: bool = True,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
    max_length: Optional[int] = None,
) -> Union[pd.DataFrame, pl.DataFrame]:
    """Clean column names to make them easier to handle.

    Args:
        df: DataFrame to clean column names for
        case: Case style ('snake', 'camel', 'pascal', 'upper', 'lower')
        remove_special: Whether to remove special characters and accents
        prefix: Prefix to add to all column names
        suffix: Suffix to add to all column names
        max_length: Maximum length for column names

    Returns:
        DataFrame with cleaned column names

    Examples:
        >>> df = pd.DataFrame({"First Name": [], "Last.Name": [], "Age!": []})
        >>> clean_names(df)
        DataFrame with columns ['first_name', 'last_name', 'age']

        >>> clean_names(df, case='pascal')
        DataFrame with columns ['FirstName', 'LastName', 'Age']

    """
    # Validate input
    if not isinstance(df, (pd.DataFrame, pl.DataFrame)):
        raise TypeError("Input must be either a pandas DataFrame or a polars DataFrame")

    if case not in ("snake", "camel", "pascal", "upper", "lower"):
        raise ValueError("Case must be one of: snake, camel, pascal, upper, lower")

    # Get current column names
    if isinstance(df, pd.DataFrame):
        columns = df.columns.tolist()
    else:
        columns = df.columns

    def clean_single_name(name: str, skip_case: bool = False) -> str:
        # Convert to string if not already
        name = str(name).strip()

        # Handle special characters
        if remove_special:
            name = unicodedata.normalize('NFKD', name).\
                encode('ASCII', 'ignore').decode('ASCII')
        else:
            # Keep combined characters intact
            name = unicodedata.normalize('NFKC', name)

        # Replace spaces and special characters with underscore
        # Only if we're removing special characters or if the character is a space
        if remove_special:
            name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        else:
            # Replace only spaces and common punctuation, preserve other special chars
            name = re.sub(r'[\s\.,!@#$%^&*()+=\[\]{};:\'\"<>?~`]', '_', name)

        # Replace multiple underscores with single one
        name = re.sub(r'_+', '_', name)

        # Remove leading/trailing underscores
        name = name.strip('_')

        if not skip_case:
            # Apply case conversion
            if case == 'snake':
                words = name.lower().split('_')
                name = '_'.join(w for w in words if w)
            elif case == 'camel':
                words = name.lower().split('_')
                name = words[0] + ''.join(w.capitalize() for w in words[1:])
            elif case == 'pascal':
                words = name.lower().split('_')
                name = ''.join(w.capitalize() for w in words)
            elif case == 'upper':
                name = name.upper()
            elif case == 'lower':
                name = name.lower()

        # Ensure the name starts with a letter or underscore
        if not name or name[0].isdigit():
            name = f"col_{name}"

        # Add prefix/suffix if provided
        if prefix:
            name = f"{prefix}{name}"
        if suffix:
            name = f"{name}{suffix}"

        # Truncate if max_length is specified
        if max_length and len(name) > max_length:
            # Ensure we don't cut in the middle of a word
            name = name[:max_length]
            if '_' in name:
                name = name.rsplit('_', 1)[0]

        return name

    # Clean all column names
    new_names = [clean_single_name(col) for col in columns]

    # Handle duplicate names
    seen = {}
    unique_names = []
    for name in new_names:
        if name in seen:
            # Increment counter before using it
            seen[name] += 1
            # Construct numbered name according to case style
            if case in ('upper', 'pascal', 'camel'):
                numbered_name = f"{name}{seen[name]}"
            else:
                numbered_name = f"{name}_{seen[name]}"
            unique_names.append(numbered_name)
        else:
            seen[name] = 1
            unique_names.append(name)

    # Apply renaming
    if isinstance(df, pd.DataFrame):
        return df.rename(columns=dict(zip(columns, unique_names)))
    else:
        rename_dict = {old: new for old, new in zip(columns, unique_names)}
        return df.rename(rename_dict)


def rename_all(
    df: Union[pd.DataFrame, pl.DataFrame],
    pattern: Union[str, dict[str, str], Callable[[str], str]],
    *,
    case: Optional[str] = None,
    remove_special: bool = False,
) -> Union[pd.DataFrame, pl.DataFrame]:
    """Rename all columns in a DataFrame according to a pattern."""
    if isinstance(df, pd.DataFrame):
        columns = df.columns.tolist()
    else:
        columns = list(df.columns)

    def transform_to_case(name: str, from_pattern: bool = False) -> str:
        """Transform a string to the specified case.

        Args:
            name: string to transform
            from_pattern: if True, indicates the name comes from a regex pattern match

        """
        # Si le nom vient d'un pattern et case n'est pas spécifié, on le retourne
        # tel quel
        if from_pattern and not case:
            return name

        # Gestion spéciale pour les colonnes numériques sauf si venant d'un pattern
        if not from_pattern and name.isdigit():
            if case == 'lower':
                return f"col_{name}"
            elif case == 'upper':
                return f"COL_{name}"
            elif case == 'title':
                return f"Col_{name}"
            return name

        # Pour les colonnes non-numériques ou venant d'un pattern
        if case == 'lower':
            return name.lower()
        elif case == 'upper':
            return name.upper()
        elif case == 'title':
            if name.isdigit():  # Pour les nombres en title case
                return f"Col_{name}"
            parts = name.split('_')
            return '_'.join(part.title() for part in parts if part)
        return name

    # Étape 1: Application du pattern
    if isinstance(pattern, str):
        try:
            new_names = []
            for col in columns:
                match = re.match(pattern, col)
                if match and match.groups():
                    # Le nom vient d'un pattern
                    name = match.group(1)
                    new_names.append(transform_to_case(name, from_pattern=True))
                else:
                    # Le nom ne vient pas d'un pattern
                    new_names.append(transform_to_case(col, from_pattern=False))
        except (IndexError, AttributeError):
            new_names = [transform_to_case(col, from_pattern=False) for col in columns]
    elif isinstance(pattern, dict):
        new_names = [transform_to_case(pattern.get(col, col), from_pattern=False)
                    for col in columns]
    elif callable(pattern):
        new_names = [transform_to_case(pattern(col), from_pattern=False)
                    for col in columns]
    else:
        raise TypeError("pattern must be string, dict, or callable")

    # Étape 2: Nettoyage des caractères spéciaux
    if remove_special:
        new_names = [
            re.sub(r'[^a-zA-Z0-9_]', '_', name).strip('_')
            for name in new_names
        ]
        new_names = [re.sub(r'_+', '_', name) for name in new_names]

    # Application finale du renommage
    if isinstance(df, pd.DataFrame):
        result = df.rename(columns=dict(zip(columns, new_names)))
    else:
        rename_dict = {old: new for old, new in zip(columns, new_names)}
        result = df.rename(rename_dict)

    return result

