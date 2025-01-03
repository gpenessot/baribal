# Installation Guide

## Requirements

Baribal requires Python 3.8 or later and has the following dependencies:

- pandas >= 2.0.0
- polars >= 0.20.0 (optional)
- numpy >= 1.22.0
- scipy >= 1.8.0

## Installing with pip

The simplest way to install Baribal is using pip:

```bash
pip install baribal
```

## Installing with UV (recommended)

Baribal can be installed using the UV package manager for faster and more reliable dependency resolution:

```bash
uv pip install baribal
```

## Development Installation

If you want to contribute to Baribal or install the latest development version:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/baribal.git
cd baribal
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
uv pip install -e ".[dev]"
```

## Verifying Installation

You can verify your installation by running Python and importing Baribal:

```python
import baribal as bb
print(bb.__version__)
```

This should display the current version number of your Baribal installation.

## Optional Dependencies

Baribal works with both pandas and polars DataFrames. While pandas is required, polars support is optional. To use Baribal with polars, make sure to install it:

```bash
pip install polars
```

## Troubleshooting

If you encounter any issues during installation:

1. Make sure you have the latest pip version:
```bash
pip install --upgrade pip
```

2. If you're having dependency conflicts, try using UV:
```bash
pip install uv
uv pip install baribal
```

3. If problems persist, please [open an issue](https://github.com/yourusername/baribal/issues) with details about your environment and the error message.