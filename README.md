# PythonTools 

# Setup
## Basic tools
- Install VSCode
- Install uv

## Install python tools
- uvx ruff
- uv tool install ruff

# Using UV vs PIP and VENV
## Installing python versions
- uv python list
- uv python install <version>

## Running a python file
- uv run <file.py>

## Installing a dependency
- uv add <package1> <package2>

## Removing a dependency
- uv remove <package1>

## Getting your .venv match hyour project.toml and .python-version
- uv sync

## seeing your dependancy tree
- uv tree

# Setting VENV to a specific version
- uv venv --python <version_number>

# Running Tools
## Checker
- uvx ruff check <file.py>
- uvx ruff check .

## Formatter
- uvx ruff format <file.py>
- uvx ruff format .



