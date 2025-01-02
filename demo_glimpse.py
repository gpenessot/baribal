"""Demo script for testing glimpse function."""
import pandas as pd
import polars as pl
from datetime import datetime, date
import numpy as np

from baribal.core import glimpse

# Créons un DataFrame avec différents types de données
data = {
    'id': range(1, 6),
    'name': ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown', 'Charlie Davis'],
    'age': [25, 30, 35, 28, 42],
    'date_joined': [date(2023, 1, 1), date(2023, 2, 15), date(2023, 3, 30), 
                   date(2023, 4, 10), date(2023, 5, 20)],
    'last_login': [datetime.now() for _ in range(5)],
    'is_active': [True, True, False, True, True],
    'score': [92.5, 88.0, None, 95.5, 90.0],
    'tags': [['dev', 'python'], ['dev', 'java'], ['design'], 
            ['dev', 'python', 'data'], ['admin']],
}

# Création du DataFrame pandas
pdf = pd.DataFrame(data)

# Création du DataFrame polars
# Note: Polars gère les listes différemment, conversion nécessaire
data_polars = data.copy()
data_polars['tags'] = [', '.join(tags) for tags in data['tags']]
pldf = pl.DataFrame(data_polars)

print("\n=== Test avec Pandas DataFrame ===")
glimpse(pdf)

print("\n=== Test avec Polars DataFrame ===")
glimpse(pldf)

# Test avec un DataFrame vide
print("\n=== Test avec un DataFrame vide (Pandas) ===")
glimpse(pd.DataFrame())

# Test avec des valeurs manquantes
print("\n=== Test avec beaucoup de valeurs manquantes (Pandas) ===")
missing_df = pd.DataFrame({
    'col1': [1, None, 3, None, 5],
    'col2': [None, 'B', None, 'D', None],
    'col3': [1.5, 2.5, None, None, 5.5]
})
glimpse(missing_df)

# Test avec des chaînes très longues
print("\n=== Test avec des chaînes longues (Polars) ===")
long_text_df = pl.DataFrame({
    'id': range(3),
    'description': [
        "This is a very long description that should be truncated in the output " * 3,
        "Another long piece of text that goes on and on " * 4,
        "Yet another lengthy piece of text that should also be truncated " * 2
    ]
})
glimpse(long_text_df)