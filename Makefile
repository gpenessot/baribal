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
