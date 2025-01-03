# baribal 🐻

A Python package extending pandas with helper functions for simpler exploratory data analysis and data wrangling.

## Why Baribal?

While pandas is incredibly powerful, some R functions like `glimpse()`, `tabyl()`, or `clean_names()` make data exploration and manipulation particularly smooth. Baribal brings these functionalities to Python, helping you to:

- Get quick, insightful overviews of your DataFrames
- Perform common data cleaning tasks with less code
- Handle missing values more intuitively
- Generate summary statistics with minimal effort

## Features

- 🔍 `glimpse()`: R-style enhanced DataFrame preview
- 🧹 Smart column naming and cleaning utilities
- 📊 Enhanced statistical summaries
- 🔮 Better missing values handling
- More coming soon...

## Installation

```bash
pip install baribal
```

## Quick Start

```python
import pandas as pd
import baribal as bb

# Get an intuitive overview of your DataFrame
bb.glimpse(df)

# More examples coming soon...
```

```
Observations: 5
Variables: 8
DataFrame type: polars
$ id          <int> 1, 2, 3, 4, 5
$ name        <chr> "John Doe", "Jane Smith", "Bob Wilson", "Alice Brown", "Charlie Davis"
$ age         <int> 25, 30, 35, 28, 42
$ date_joined <dte> 2023-01-01, 2023-02-15, 2023-03-30, 2023-04-10, 2023-05-20
$ last_login  <dtm> 2025-01-03 01:06:..., 2025-01-03 01:06:..., 2025-01-03 01:06:..., 2025-01-03 01:06:..., 2025-01-03 01:06:...
$ is_active   <log> True, True, False, True, True
$ score       <num> 92.5, 88.0, NA, 95.5, 90.0
$ tags        <chr> "dev, python", "dev, java", "design", "dev, python, data", "admin"
```

## Development

This project uses modern Python development tools:
- `uv` for fast, reliable package management
- `ruff` for lightning-fast linting and formatting
- `pytest` for testing

To set up the development environment:

```bash
make install
```

## Contributing

Contributions are welcome! Whether it's suggesting new features, improving documentation, or reporting bugs.

Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our git commit conventions and development process.

## License

MIT License
