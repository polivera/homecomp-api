run:
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

migration-generate comment:
    alembic revision -m "{{comment}}"

migrate:
    uv run alembic upgrade head

migrate-test:
    DB_PORT=5434 DB_NAME=homecomp_test uv run alembic upgrade head

seed:
    uv run python -m scripts.seed

pgcli:
    pgcli postgresql://$DB_USER:$DB_PASS@$DB_HOST:$DB_PORT/$DB_NAME

pgcli-test:
    pgcli postgresql://$DB_USER:$DB_PASS@$DB_HOST:5433/homecomp_test

test-unit:
    uv run pytest -m unit

test-integration:
    uv run pytest -m integration
