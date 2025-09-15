# Coffee Shop API Makefile

.PHONY: help test test-unit test-integration test-coverage test-verbose test-fast lint format install-dev run-server

# Default target
help:
	@echo "Available targets:"
	@echo "  test           - Run all tests"
	@echo "  test-unit      - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-coverage  - Run tests with coverage report"
	@echo "  test-verbose   - Run tests in verbose mode"
	@echo "  test-fast      - Run tests excluding slow tests"
	@echo "  lint           - Run linting checks"
	@echo "  format         - Format code with black"
	@echo "  install-dev    - Install development dependencies"
	@echo "  run-server     - Start the FastAPI server"

# Test targets
test:
	uv run python run_tests.py --type all

test-unit:
	uv run python run_tests.py --type unit

test-integration:
	uv run python run_tests.py --type integration

test-coverage:
	uv run python run_tests.py --type coverage

test-verbose:
	uv run python run_tests.py --type all --verbose

test-fast:
	uv run python run_tests.py --type all --fast

# Development targets
lint:
	uv run flake8 main.py models.py
	uv run black --check main.py models.py

format:
	uv run black main.py models.py

install-dev:
	uv add flake8 black pytest-cov

# Server target
run-server:
	uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
