#!/bin/bash

# Run flake8 on project files only, using the configuration from setup.cfg
./.venv/bin/flake8 --config=setup.cfg .

# Run mypy with the same configuration as in the Makefile
./.venv/bin/mypy . --explicit-package-bases --namespace-packages

# Exit with the combined status
exit $?
