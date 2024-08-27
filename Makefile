# Makefile for Update Sensei project

PYTHON := python3
VENV := venv
VENV_BIN := $(VENV)/bin

PROJECT_NAME := update_sensei
SRC_DIR := src
TEST_DIR := tests
EXAMPLES_DIR := examples

PIP := $(VENV_BIN)/pip
PYTHON_VENV := $(VENV_BIN)/python
BLACK := $(VENV_BIN)/black
ISORT := $(VENV_BIN)/isort
FLAKE8 := $(VENV_BIN)/flake8
PYTEST := $(VENV_BIN)/pytest

.PHONY: all venv install clean format lint test run-examples

all: venv install format lint test

venv:
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV)
	@echo "To activate the virtual environment, run:"
	@echo "source $(VENV_BIN)/activate"

install: venv
	@echo "Installing dependencies..."
	@$(VENV_BIN)/pip install --upgrade pip
	@$(VENV_BIN)/pip install -r requirements.txt
	@$(VENV_BIN)/pip install -e .

clean:
	@echo "Cleaning cache files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete

format:
	@echo "Formatting code..."
	@$(VENV_BIN)/black $(SRC_DIR) $(TEST_DIR) $(EXAMPLES_DIR)
	@$(VENV_BIN)/isort $(SRC_DIR) $(TEST_DIR) $(EXAMPLES_DIR)

lint:
	@echo "Linting code..."
	@$(VENV_BIN)/flake8 $(SRC_DIR) $(TEST_DIR) $(EXAMPLES_DIR)

test:
	@echo "Running tests..."
	@$(VENV_BIN)/pytest $(TEST_DIR)
