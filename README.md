# baribal 🐻

A Python package extending pandas with R-inspired helper functions for simpler exploratory data analysis and data wrangling.

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