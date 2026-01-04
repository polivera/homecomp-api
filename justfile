# List all available commands
default:
    @just --list

# ============================================================================
# Development Server
# ============================================================================

# Start development server with auto-reload
dev:
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Start development server with debug environment
dev-debug:
    APP_ENV=debug uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Start development server with test environment
dev-test:
    APP_ENV=test uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# ============================================================================
# Database Migrations
# ============================================================================

# Generate a new database migration
migrate-new comment:
    alembic revision -m "{{comment}}"

# Run pending migrations
migrate:
    uv run alembic upgrade head

# Run pending migrations (test environment)
migrate-test:
    APP_ENV=test uv run alembic upgrade head

# ============================================================================
# Database Operations
# ============================================================================

# Connect to PostgreSQL database (dev)
db:
    pgcli postgresql://$DB_USER:$DB_PASS@$DB_HOST:$DB_PORT/$DB_NAME

# Connect to PostgreSQL database (test)
db-test:
    pgcli postgresql://$TEST_DB_USER:$TEST_DB_PASS@$TEST_DB_HOST:$TEST_DB_PORT/$TEST_DB_NAME

# Clear all data from database
db-clear:
    uv run python scripts/db_clear.py

# Seed database with initial data
db-seed:
    uv run python scripts/seed.py

# Clear and reseed database
db-reset:
    just db-clear
    just db-seed

# ============================================================================
# Testing
# ============================================================================

# Run unit tests
test:
    uv run pytest -m unit --ignore=tests/integration

# Run unit tests with coverage report
test-cov:
    uv run pytest -m unit --ignore=tests/integration --cov --cov-report=term --cov-report=html

# Run integration tests
test-integration:
    APP_ENV=test uv run pytest -m integration

# ============================================================================
# Code Quality
# ============================================================================

# Check code with linter
lint:
    uv run ruff check .

# Check code formatting
fmt-check:
    uv run ruff format --check .

# Run all checks (lint + format)
check:
    uv run ruff check .
    uv run ruff format --check .

# Auto-fix linting issues
lint-fix:
    uv run ruff check --fix .

# Auto-format code
fmt:
    uv run ruff format .

# Auto-fix linting and formatting
fix:
    uv run ruff check --fix .
    uv run ruff format .
