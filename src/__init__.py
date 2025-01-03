"""Baribal: R-inspired data analysis utilities for Python."""

from baribal.core import glimpse, tabyl
from baribal.utils import clean_names, rename_all  #, standardize_types, case_when
from baribal.viz import missing_summary  #, correlation_quick, quick_profile

__version__ = "0.1.0"

__all__ = [
    # Core functions
    "glimpse",
    "tabyl",

    # Visualization functions
    "missing_summary",
    #"correlation_quick",
    #"quick_profile",

    # Utility functions
    "clean_names",
    "rename_all",
    #"standardize_types",
    #"case_when",
]
