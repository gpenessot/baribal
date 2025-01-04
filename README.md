![](images/logo%20baribal.png)

# baribal 🐻

[![Build Status](https://img.shields.io/github/actions/workflow/status/gpenessot/baribal/main.yml?branch=main)](https://github.com/gpenessot/baribal/actions)
[![PyPI version](https://img.shields.io/pypi/v/baribal)](https://pypi.org/project/baribal/)
[![PyPI downloads](https://img.shields.io/pypi/dm/baribal)](https://pypi.org/project/baribal/)
[![Coverage](https://img.shields.io/codecov/c/github/gpenessot/baribal)](https://codecov.io/gh/gpenessot/baribal)
[![License](https://img.shields.io/github/license/gpenessot/baribal)](https://github.com/gpenessot/baribal/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/baribal)](https://pypi.org/project/baribal/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A Python package extending pandas and polars with helper functions for simpler exploratory data analysis and data wrangling, inspired by R's tidyverse packages.

## Why Baribal?

While pandas and polars are incredibly powerful, some R functions like `glimpse()`, `tabyl()`, or `clean_names()` make data exploration and manipulation particularly smooth. Baribal brings these functionalities to Python, helping you to:

- Get quick, insightful overviews of your DataFrames
- Perform common data cleaning tasks with less code
- Handle missing values more intuitively
- Generate summary statistics with minimal effort

## Features

### Core Functions

#### 🔍 `glimpse()`
R-style enhanced DataFrame preview that works with both pandas and polars:

```python
import pandas as pd
import baribal as bb

df = pd.DataFrame({
    'id': range(1, 6),
    'name': ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown', 'Charlie Davis'],
    'age': [25, 30, 35, 28, 42],
    'score': [92.5, 88.0, None, 95.5, 90.0]
})

bb.glimpse(df)
```

Output:
```
Observations: 5
Variables: 4
DataFrame type: pandas
$ id    <int> 1, 2, 3, 4, 5
$ name  <chr> "John Doe", "Jane Smith", "Bob Wilson", "Alice Brown", "Charlie Davis"
$ age   <int> 25, 30, 35, 28, 42
$ score <num> 92.5, 88.0, NA, 95.5, 90.0
```

#### 📊 `tabyl()`
Enhanced cross-tabulations with integrated statistics:

```python
import baribal as bb

# Single variable frequency table
result, _ = bb.tabyl(df, 'category')

# Two-way cross-tabulation with chi-square statistics
result, stats = bb.tabyl(df, 'category', 'status')
```

### Data Cleaning

#### 🧹 `clean_names()`
Smart column name cleaning with multiple case styles:

```python
import baribal as bb

df = pd.DataFrame({
    "First Name": [],
    "Last.Name": [],
    "Email@Address": [],
    "Phone #": []
})

# Snake case (default)
bb.clean_names(df)
# → columns become: ['first_name', 'last_name', 'email_address', 'phone']

# Camel case
bb.clean_names(df, case='camel')
# → columns become: ['firstName', 'lastName', 'emailAddress', 'phone']

# Pascal case
bb.clean_names(df, case='pascal')
# → columns become: ['FirstName', 'LastName', 'EmailAddress', 'Phone']
```

#### 🔄 `rename_all()`
Batch rename columns using patterns:

```python
import baribal as bb

# Using regex pattern
bb.rename_all(df, r'Col_(\d+)')  # Extracts numbers from column names

# Using case transformation
bb.rename_all(df, lambda x: x.lower())  # Convert all to lowercase
```

### Analysis Tools

#### 🔍 `missing_summary()`
Comprehensive missing values analysis:

```python
import baribal as bb

summary = bb.missing_summary(df)
# Returns DataFrame with missing value statistics for each column
```

## Installation

```bash
pip install baribal
```

## Dependencies

- Python >= 3.8
- pandas >= 1.0.0
- polars >= 0.20.0 (optional)
- numpy
- scipy

## Development

This project uses modern Python development tools:
- `uv` for fast, reliable package management
- `ruff` for lightning-fast linting and formatting
- `pytest` for testing

To set up the development environment:

```bash
make install
```

To run tests:

```bash
make test
```

## Contributing

Contributions are welcome! Whether it's:
- Suggesting new R-inspired features
- Improving documentation
- Adding test cases
- Reporting bugs

Please check out our [Contributing Guidelines](CONTRIBUTING.md) for details on our git commit conventions and development process.

## License

MIT License

## Acknowledgments

Inspired by various R packages including:
- `dplyr`
- `janitor`
- `tibble`
- `naniar`