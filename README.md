# totes-app

Tote Tracker is a self-hosted inventory app for organizing storage totes with QR codes, searchable items, and checkout history.

## Docs

- Product requirements: `docs/prd.md`
- Requirements & design plan: `docs/RDP.md`
- Development phases: `docs/PHASES.md`
- Draft database schema (Postgres): `db/schema.sql`
- Environment template: `.env.example`
- Make targets: `Makefile`

## Getting started

- Review the docs to confirm scope and technical choices.
- Use `db/schema.sql` as the initial schema reference when scaffolding migrations.

## How to run locally

Backend stack: Python (FastAPI)

Prereqs:
- Python 3.11+
- Postgres 15+

Local setup (example):
1) Create and activate a virtualenv
2) Install dependencies: `pip install -r backend/requirements.txt`
3) Set env vars: `DATABASE_URL`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`
4) Apply `db/migrations/0001_init.sql` to your Postgres database
5) Start the API: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

Docker (Portainer) plan:
- One app container running FastAPI
- One Postgres container
- Bind a NAS-backed volume for uploads

Docker (Portainer) quick start:
1) Create a new stack from `docker-compose.yml`
2) Adjust the `uploads` volume to a bind mount on your NAS (Portainer UI)
3) Create a `.env` file from `.env.example` and update values
4) Deploy the stack
