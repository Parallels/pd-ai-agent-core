# Contributing to pd-ai-agent-core

Thank you for your interest in contributing to pd-ai-agent-core! This document provides guidelines and instructions for contributing to this project.

## Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/cjlapao/pd-ai-agent-core.git
   cd pd-ai-agent-core
   ```

2. Create and activate a virtual environment:

   ```bash
   make setup
   source .venv/bin/activate  # On Windows: `.venv\Scripts\activate`
   ```

3. Install development dependencies:

   ```bash
   make dev-install
   ```

4. Install pre-commit hooks:

   ```bash
   make install-hooks
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and ensure they follow our coding standards:

   ```bash
   make format  # Format code using black
   make lint    # Run linting checks
   make test    # Run tests
   ```

3. Commit your changes:

   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

4. Push your changes and create a Pull Request:

   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style Guidelines

- We use `black` for code formatting
- We use `flake8` for code linting
- We use `mypy` for type checking
- Follow PEP 8 guidelines
- Write meaningful commit messages
- Include docstrings for public functions and classes
- Add type hints to function parameters and return values

## Testing

- Write tests for new features
- Ensure all tests pass before submitting a PR
- Maintain or improve code coverage

## Documentation

- Update documentation for new features or changes
- Include docstrings in your code
- Update README.md if necessary

## Package Publishing

The package is published to PyPI using GitHub Actions. The workflow is triggered when a new release is created.

To create a new release:

1. Update version in `setup.py`
2. Create and push a new tag:

   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. Create a new release on GitHub with release notes

## Questions or Problems?

Feel free to open an issue if you have any questions or encounter any problems.

Thank you for contributing!
