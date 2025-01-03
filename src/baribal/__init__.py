"""Baribal: R-inspired data analysis utilities for Python."""

from baribal.core import glimpse, tabyl
from baribal.utils import clean_names, rename_all, memory_diet
from baribal.viz import missing_summary

__version__ = "0.1.0"

__all__ = [
    "glimpse",
    "tabyl",
    "clean_names",
    "rename_all",
    "memory_diet",
    "missing_summary",
]
