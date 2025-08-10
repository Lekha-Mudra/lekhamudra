# Lekhamudra Backend (FastAPI)

FastAPI + SQLAlchemy 2.x + Alembic + uv. Provides session‑based authentication and document APIs for the Lekhamudra platform.

## Features

- PostgreSQL persistence (SQLAlchemy ORM + Alembic migrations)
- Modular application layout (api / core / crud / db / models / schemas)
- Session cookie authentication (server-side sessions table, no JWT)
- Pydantic v2 & settings management
- uv for fast, reproducible dependency management
- Basic test suite (pytest + httpx integration)
- Pre-commit hooks (Ruff lint/format, pyupgrade, hygiene checks)

## Architecture

```
backend/
  main.py              # App entrypoint
  alembic/             # Migration environment & versions
  app/
	 api/               # Routers (versioned under v1) + dependencies
	 core/              # Config, security helpers
	 crud/              # Data access operations
	 db/                # Session factory
	 models/            # SQLAlchemy models (user, document, session)
	 schemas/           # Pydantic models
```

## Quick Start

Prerequisites: Python 3.10+, PostgreSQL (local or Docker), `uv` installed.

1. Copy configuration example and edit values:
   ```bash
   cp .env.example .env
   # fill in database credentials (do not commit secrets)
   ```
2. Start Postgres (Docker example):
   ```bash
   docker compose up -d
   ```
3. Install dependencies:
   ```bash
   uv sync
   ```
4. (Optional) Apply migrations explicitly (recommended outside pure dev):
   ```bash
   uv run alembic upgrade head
   ```
   In dev the app can auto-create tables if they don't yet exist.
5. Run the API:
   ```bash
   uv run uvicorn main:app --reload
   ```

API base: `http://localhost:8000`
Docs (Swagger): `http://localhost:8000/docs`

## Configuration

Environment variables (see `.env.example`):

| Category | Variables (names only)                                                      | Notes                        |
| -------- | --------------------------------------------------------------------------- | ---------------------------- |
| Database | POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT | Combined into runtime DB URL |
| Runtime  | ENV, LOG_LEVEL                                                              | Optional tuning              |

Guidelines:

1. Update `.env.example` when introducing new variables (placeholder values only).
2. Keep production secrets outside git (deployment secret manager).

## Auth Flow

1. User signs up or logs in via form POST.
2. Backend creates session row (`sessions` table) and sets `session_id` HttpOnly cookie.
3. Client checks `/api/v1/auth/me` for `{ authenticated, user }`.
4. Logout deletes the session + clears cookie.

Session lifetime: fixed TTL (7 days) until rotation/refresh logic is added.

## Endpoints (v1)

| Method | Path                | Description                         |
| ------ | ------------------- | ----------------------------------- |
| POST   | /api/v1/auth/signup | Register & set session cookie       |
| POST   | /api/v1/auth/login  | Login & set session cookie          |
| POST   | /api/v1/auth/logout | Invalidate current session          |
| GET    | /api/v1/auth/me     | Auth status & user info             |
| CRUD   | /api/v1/documents   | Document operations (auth required) |
| GET    | /ping               | Health probe                        |

## Alembic Migrations

Create a new migration after model changes:

```bash
uv run alembic revision --autogenerate -m "describe change"
uv run alembic upgrade head
```

Check current head:

```bash
uv run alembic current
```

## Testing

Run all tests:

```bash
uv run -m pytest -q
```

Add tests for each new endpoint (happy path + unauthorized case at minimum).

## Pre-commit Hooks

Install and run once:

```bash
pip install pre-commit  # or use uv tool install pre-commit
pre-commit install --install-hooks
pre-commit run --all-files
```

Configured hooks: Ruff (lint+format), pyupgrade (py310), trailing whitespace, EOF fixer, YAML/TOML/JSON/XML checks, private key & debug statement detection.

## Common Commands

| Action             | Command                                           |
| ------------------ | ------------------------------------------------- |
| Run dev server     | `uv run uvicorn main:app --reload`                |
| New migration      | `uv run alembic revision --autogenerate -m "msg"` |
| Apply migrations   | `uv run alembic upgrade head`                     |
| Tests              | `uv run -m pytest -q`                             |
| Lint/format (ruff) | `uv run ruff check . --fix && uv run ruff format` |

## Development Notes

- Dev auto-creation of tables is convenience only; rely on migrations elsewhere.
- Keep migrations deterministic (avoid non-deterministic default timestamps in autogenerate where feasible).
- Avoid leaking real credentials in commit diffs or PR descriptions.

## Roadmap (Backend Focus)

- Rolling session extension & pruning task
- Document sharing permissions & audit metadata
- OCR ingestion pipeline (async workers)
- File/object storage integration
- Expanded test matrix & performance profiling

## Contributing

1. Branch from `main`: `feat/<short-description>`.
2. Make changes + add/adjust tests.
3. Run hooks & tests locally.
4. Open PR with concise summary; link any related issue.

---

See root `README.md` for full-stack overview.
