.PHONY: run deps db migrate test

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

deps:
	pip install -r backend/requirements.txt

db:
	docker compose up -d db

migrate:
	psql "$$DATABASE_URL" -f db/migrations/0001_init.sql

test:
	@if [ -x ".venv/bin/python" ] && .venv/bin/python -c "import pytest" >/dev/null 2>&1; then \
		PYTHONPATH=backend .venv/bin/python -m pytest -q backend/tests/test_smoke.py; \
	else \
		PY_SITE=$$(ls -d .venv/lib/python*/site-packages 2>/dev/null | head -n 1); \
		if [ -n "$$PY_SITE" ]; then \
			PYTHONPATH="backend:$$PY_SITE" pytest -q backend/tests/test_smoke.py; \
		else \
			PYTHONPATH=backend pytest -q backend/tests/test_smoke.py; \
		fi; \
	fi
