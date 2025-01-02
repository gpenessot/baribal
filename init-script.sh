#!/bin/bash

# Vérification de l'installation des dépendances
command -v git >/dev/null 2>&1 || { echo "git is required but not installed. Aborting." >&2; exit 1; }
command -v uv >/dev/null 2>&1 || { echo "uv is required but not installed. Aborting." >&2; exit 1; }

# Vérification qu'on est dans un repo git
if [ ! -d ".git" ]; then
    echo "Ce script doit être exécuté depuis la racine d'un repo git. Aborting." >&2
    exit 1
fi

echo "🐻 Initialisation du projet baribal..."

# Création des répertoires
mkdir -p src/baribal tests .github/workflows

# Création des fichiers Python initiaux
touch src/baribal/__init__.py
touch src/baribal/core.py
touch src/baribal/viz.py
touch src/baribal/utils.py
touch tests/__init__.py
touch tests/test_core.py

# Création du README.md
cat > README.md << EOL
# baribal

Helper functions for pandas data analysis, inspired by R.

## Installation

\`\`\`bash
pip install baribal
\`\`\`

## Features

- \`glimpse()\`: R-style DataFrame overview
- More coming soon...

## Development

This project uses:
- \`uv\` for package management
- \`ruff\` for linting and formatting
- \`pytest\` for testing

To set up the development environment:

\`\`\`bash
make install
\`\`\`

## License

MIT License
EOL

# Création du .gitignore
cat > .gitignore << EOL
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Tests
.pytest_cache/
.coverage
htmlcov/

# Environments
.env
.venv
env/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Ruff
.ruff_cache/
EOL

# Création du pyproject.toml
cat > pyproject.toml << EOL
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "baribal"
version = "0.1.0"
description = "Helper functions for pandas data analysis, inspired by R"
readme = "README.md"
requires-python = ">=3.9"
license = "MIT"
keywords = ["pandas", "data-analysis", "r", "glimpse"]
authors = [
    { name = "Gaël Penessot", email = "gael.penessot@data-decision.io" }
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Scientific/Engineering :: Data Science",
]
dependencies = [
    "pandas>=2.0.0",
    "numpy>=1.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 88
target-version = "py39"
select = ["E", "F", "B", "I", "UP", "N", "W", "D"]
ignore = ["D100", "D104"]

[tool.ruff.per-file-ignores]
"tests/*" = ["D", "B", "S"]

[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --cov=baribal"
testpaths = [
    "tests",
]
EOL

# Création du Makefile
cat > Makefile << EOL
.PHONY: install format lint test clean

install:
	uv venv
	uv pip install -e ".[dev]"

format:
	ruff format src tests
	ruff check --fix src tests

lint:
	ruff check src tests

test:
	pytest

clean:
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf .ruff_cache
	rm -rf dist
	rm -rf *.egg-info
EOL

# Ajout des fichiers au git
git add .
git commit -m "Initial commit 🐻"

# Création de l'environnement virtuel et installation des dépendances
make install

echo "✨ Projet baribal initialisé avec succès!"
echo "📁 Structure du projet créée"
echo "📦 Dépendances installées"
echo "🔨 Makefile configuré"
echo "🐍 Environnement virtuel créé"
echo ""
echo "Prochaine étape:"
echo "1. Commencer l'implémentation de glimpse()"