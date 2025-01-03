# Baribal Demos

This directory contains demonstration scripts showing how to use various features of the Baribal package.

## Available Demos

- `demo_tabyl.py`: Examples of frequency tables and cross-tabulations
- `demo_glimpse.py`: Examples of DataFrame inspection and overview
- `demo_clean_names.py`: Examples of column name cleaning and standardization

## Running the Demos

Each demo can be run independently. Make sure you have Baribal installed:

```bash
pip install baribal
```

Then run any demo script:

```bash
python demo_tabyl.py
```

## Sample Data

The `data/` directory contains sample datasets used in the demos:

- `sample_data.csv`: Main dataset used across different demos

## Creating New Demos

When creating new demos:

1. Create a new Python file with a clear name (e.g., `demo_feature.py`)
2. Include docstrings explaining the purpose of the demo
3. Add sample data to `data/` if needed
4. Update this README.md with information about your demo