run:
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

migration-generate comment:
    alembic revision -m "{{comment}}"

migrate:
    alembic upgrade head

pgcli:
    pgcli postgresql://$DB_USER:$DB_PASS@$DB_HOST:$DB_PORT/$DB_NAME
