.PHONY: setup clean test lint format install dev-install changelog version-bump version activate deactivate

# Python interpreter and venv settings
PYTHON := python3
VENV := .venv
VENV_BIN := $(VENV)/bin

# OS specific settings
ifeq ($(OS),Windows_NT)
	VENV_ACTIVATE = $(VENV)/Scripts/activate
	VENV_PYTHON = $(VENV)/Scripts/python
else
	VENV_ACTIVATE = $(VENV)/bin/activate
	VENV_PYTHON = $(VENV)/bin/python
endif

# Version management
VERSION_FILE := VERSION
SETUP_FILE := setup.py
CURRENT_VERSION := $(shell cat $(VERSION_FILE))
MAJOR := $(shell echo $(CURRENT_VERSION) | cut -d. -f1)
MINOR := $(shell echo $(CURRENT_VERSION) | cut -d. -f2)
PATCH := $(shell echo $(CURRENT_VERSION) | cut -d. -f3)

# Install production dependencies
setup: $(VENV)/bin/activate
	$(VENV_BIN)/pip install -r requirements.txt
	@echo "Virtual environment created and dependencies installed."
	@echo "To activate the virtual environment, run:"
	@echo "  source $(VENV_ACTIVATE)"

# Create virtual environment
$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install black flake8 pytest mypy build twine

# Clean up generated files and virtual environment
clean:
	rm -rf $(VENV)
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run tests
test:
	$(VENV_BIN)/pytest

# Run linting
lint:
	@.github/scripts/lint.sh

# Format code using black
format:
	$(VENV_BIN)/black .

# Install package in development mode
dev-install:
	$(VENV_BIN)/pip install -e .

# Build package
build:
	$(VENV_BIN)/python -m build

# Original build target that cleans first (renamed for reference)
build-clean: clean
	$(VENV_BIN)/python -m build

# Upload to PyPI (requires credentials)
publish: build
	$(VENV_BIN)/twine upload dist/*

# Install pre-commit hooks
install-hooks:
	$(VENV_BIN)/pip install pre-commit
	$(VENV_BIN)/pre-commit install

# Generate changelog
changelog:
	@echo "Generating changelog..."
	@chmod +x .github/scripts/generate_changelog.sh
	@.github/scripts/generate_changelog.sh --version $(CURRENT_VERSION)

# Version bump
version-bump:
	@if [ "$(TYPE)" = "major" ]; then \
		NEW_VER="$$(($(MAJOR)+1)).0.0"; \
	elif [ "$(TYPE)" = "minor" ]; then \
		NEW_VER="$(MAJOR).$$(($(MINOR)+1)).0"; \
	elif [ "$(TYPE)" = "patch" ]; then \
		NEW_VER="$(MAJOR).$(MINOR).$$(($(PATCH)+1))"; \
	elif [ "$(NEW_VERSION)" != "" ]; then \
		NEW_VER="$(NEW_VERSION)"; \
	else \
		echo "Usage: make version-bump NEW_VERSION=x.x.x"; \
		echo "   or: make version-bump TYPE=[major|minor|patch]"; \
		exit 1; \
	fi; \
	echo "Current version: $(CURRENT_VERSION)"; \
	echo "New version: $$NEW_VER"; \
	echo "$$NEW_VER" > $(VERSION_FILE); \
	sed -i.bak "s/version=\"[^\"]*\"/version=\"$$NEW_VER\"/" $(SETUP_FILE) && rm $(SETUP_FILE).bak; \
	echo "Version updated to $$NEW_VER"; \
	echo "Don't forget to commit the changes and create a PR"

# Show current version
version:
	@echo "$(CURRENT_VERSION)"

# Virtual environment management
activate:
	@echo "To activate the virtual environment, run:"
	@echo "  source $(VENV_ACTIVATE)"
	@echo ""
	@echo "Note: This command must be run as 'source make activate' or '. make activate'"
	@echo "      because 'make activate' alone runs in a subshell and won't persist"

deactivate:
	@echo "To deactivate the virtual environment, simply run:"
	@echo "  deactivate"
	@echo ""
	@echo "Note: The deactivate command is available only when a virtual environment is active"

# Helper to check if venv is active
check-venv:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Virtual environment is not active. Please activate it first:"; \
		echo "  source $(VENV_ACTIVATE)"; \
		exit 1; \
	fi 