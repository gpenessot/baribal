# Baribal Documentation 🐻

Welcome to Baribal's documentation. Baribal is a Python package that brings the convenience of R's data manipulation functions to the pandas ecosystem. Named after the American black bear (*Ursus americanus*), this package aims to make data analysis in Python as intuitive and efficient as in R.

## Features

- 🔍 **DataFrame Inspection**
  - `glimpse()`: Get an R-style enhanced preview of your DataFrame
  - `missing_summary()`: Visualize and analyze missing values

- 🧹 **Data Cleaning**
  - `clean_names()`: Smart column name cleaning and standardization
  - `rename_all()`: Apply consistent renaming patterns to columns

- 📊 **Statistical Analysis**
  - `tabyl()`: Enhanced cross-tabulations with integrated statistics
  - More features coming soon...

## Quick Start

### Installation

```bash
pip install baribal
```

### Basic Usage

```python
import pandas as pd
import baribal as bb

# Create a sample DataFrame
df = pd.DataFrame({
    "First Name": ["Alice", "Bob"],
    "Last.Name": ["Smith", "Jones"],
    "Age": [25, 30]
})

# Get a quick overview
bb.glimpse(df)

# Clean column names
clean_df = bb.clean_names(df)

# Create a cross-tabulation
result, stats = bb.tabyl(df, 'First Name', 'Age')
```

## Why Baribal?

While pandas is an incredibly powerful library, some common data analysis tasks can be verbose or require multiple steps. Baribal brings R's intuitive data manipulation functions to Python, helping you to:

- Get quick, insightful overviews of your DataFrames
- Perform common data cleaning tasks with less code
- Handle missing values more intuitively
- Generate summary statistics with minimal effort

## Guides

- [Installation Guide](guide/installation.md)
- [Usage Guide](guide/usage.md)

## API Reference

- [Core Functions](api/core.md)
- [Utility Functions](api/utils.md)

## Contributing

Contributions are welcome! Whether you're fixing bugs, improving documentation, or proposing new features, please feel free to open an issue or submit a pull request.

## Support

If you encounter any issues or have questions:

1. Check the [Installation Guide](guide/installation.md) and [Usage Guide](guide/usage.md)
2. Search through our [GitHub Issues](https://github.com/yourusername/baribal/issues)
3. Open a new issue if needed

## License

Baribal is released under the MIT License. See the LICENSE file for more details.