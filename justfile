run:
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

run-with-test:
    APP_ENV=test uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

migration-generate comment:
    alembic revision -m "{{comment}}"

migrate:
    uv run alembic upgrade head

migrate-test:
    APP_ENV=test uv run alembic upgrade head

db-clear:
    uv run python scripts/db_clear.py

seed:
    uv run python scripts/seed.py

db-reset:
    just db-clear
    just seed

pgcli:
    pgcli postgresql://$DB_USER:$DB_PASS@$DB_HOST:$DB_PORT/$DB_NAME

pgcli-test:
    pgcli postgresql://$DB_USER:$DB_PASS@$DB_HOST:5433/homecomp_test

test-unit:
    uv run pytest -m unit --ignore=tests/integration

test-unit-cov:
    uv run pytest -m unit --ignore=tests/integration --cov --cov-report=term --cov-report=html

test-integration:
    APP_ENV=test uv run pytest -m integration

lint:
    uv run ruff check .

lint-fix:
    uv run ruff check --fix .

format:
    uv run ruff format .

format-check:
    uv run ruff format --check .

check:
    uv run ruff check .
    uv run ruff format --check .

fix:
    uv run ruff check --fix .
    uv run ruff format .
