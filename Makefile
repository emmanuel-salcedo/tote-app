.PHONY: run deps db migrate

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

deps:
	pip install -r backend/requirements.txt

db:
	docker compose up -d db

migrate:
	psql "$$DATABASE_URL" -f db/migrations/0001_init.sql
