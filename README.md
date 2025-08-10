<h1 align="center">Lekhamudra</h1>
<p align="center">Nepalese open‑source document sharing & (future) OCR platform – Next.js frontend + FastAPI backend + PostgreSQL</p>

## Overview

This mono‑repo contains:

| Part     | Path                     | Stack                            | Notes                               |
| -------- | ------------------------ | -------------------------------- | ----------------------------------- |
| Frontend | `/` (Next.js App Router) | Next.js 14, TypeScript, Tailwind | Auth pages, dashboard shell         |
| Backend  | `/backend`               | FastAPI, SQLAlchemy, Alembic, uv | Session cookie auth, documents CRUD |
| Database | Docker (optional)        | PostgreSQL                       | Local dev via docker-compose        |

Current authentication uses server‑side sessions stored in Postgres (no JWT). A secure `session_id` HttpOnly cookie identifies the user.

## Quick Start

### 1. Backend (API)

Copy the example configuration and adjust for your machine:

```
cd backend
cp .env.example .env  # Or create manually if you prefer
```

Fill in required values (database connection, environment mode). Keep secrets out of commits.

Run Postgres (example using Docker):

```bash
docker compose up -d  # in backend/ if docker-compose.yml exists
```

Install deps (uv auto‑creates venv):

```bash
cd backend
uv sync
```

Apply migrations (optional in dev – tables auto-create):

```bash
uv run alembic upgrade head
```

Start API:

```bash
uv run uvicorn main:app --reload
```

API docs: http://localhost:8000/docs

### 2. Frontend

Root folder:

```bash
npm install
npm run dev
```

Visit http://localhost:3000

To target a non-default API host set `NEXT_PUBLIC_API_BASE` in a frontend env file (not required for local defaults). No secrets should be placed in public Next.js env vars (they are bundled client-side).

## Configuration

Back‑end configuration lives in environment variables loaded via `.env` (see `backend/.env.example`). Categories:

- Database: connection components (user, password, host, port, db name)
- App Mode: environment flag (`dev`, `prod`, etc.)
- (Future) OCR / Storage: credentials & buckets (not yet implemented – keep out of README once added; document only variable names)

Guidelines:

1. Never commit real secrets – only the `.env.example` with placeholder values.
2. Keep production secrets in your deployment platform's secret manager.
3. If you add a new env var: update `.env.example` and brief one‑line comment there; no need to repeat it verbatim here.

## Auth Flow (Session Based)

1. User signs up / logs in.
2. Backend creates a row in `sessions` table (7‑day TTL) and sets `session_id` HttpOnly cookie.
3. Frontend checks `/api/v1/auth/me` – returns `{ authenticated: true, user: {...} }` or `{ authenticated: false, user: null }` (never 401 for missing session now).
4. Logout deletes the session row and clears cookie.

Advantages: central revocation, no tokens in JS (XSS surface reduced).

## Key API Endpoints

| Method | Path                | Description                            |
| ------ | ------------------- | -------------------------------------- |
| POST   | /api/v1/auth/signup | Create account (sets session cookie)   |
| POST   | /api/v1/auth/login  | Form login (username=email)            |
| POST   | /api/v1/auth/logout | Destroy session                        |
| GET    | /api/v1/auth/me     | Auth status & user info                |
| CRUD   | /api/v1/documents   | Document operations (requires session) |
| GET    | /ping               | Health check                           |

## Project Structure (Backend)

```
backend/app/
	api/        # Routers & deps
	core/       # Config & security helpers
	models/     # SQLAlchemy models (users, documents, sessions)
	crud/       # Data access functions
	schemas/    # Pydantic models
	db/         # Session + engine
```

## Development Workflow (One Feature at a Time)

1. Create a branch: `feat/<short-description>`
2. Implement backend changes (add model -> alembic revision -> CRUD -> router -> tests).
3. Update frontend components/pages to consume new API.
4. Run tests: `uv run -m pytest -q` (add tests for new endpoints).
5. Update README / docs if public API changed.
6. Open PR referencing feature scope.

### Adding a New Model Example

```bash
uv run alembic revision --autogenerate -m "add notes"
uv run alembic upgrade head
```

Then expose via a new router under `app/api/v1/endpoints/`.

## Testing

Backend unit/integration tests (pytest) live in `backend/tests`.

```bash
cd backend
uv run -m pytest -q
```

Add at least:

- Happy path test
- Auth required test (unauthenticated -> authenticated flow)

## Pre-commit Hooks

The repository ships with a `.pre-commit-config.yaml` to enforce formatting (Ruff), code modernisation (pyupgrade), and basic hygiene checks before commits.

Setup (once):

```bash
pip install pre-commit  # or uv tool install pre-commit
pre-commit install --install-hooks
```

Run manually over the whole repo (first time, or after adding new hooks):

```bash
pre-commit run --all-files
```

Hooks run automatically on staged changes at `pre-commit` stage. If a hook auto-fixes files, re-stage and re-run commit.

Python target: 3.10 (pyupgrade / Ruff configured accordingly). Avoid introducing 3.11+/3.12-only syntax unless config is updated.

CI: Enable weekly auto-updates via the included `ci` section. (If using GitHub Actions later, add `pre-commit/action` for server-side validation.)

Add new hooks by editing `.pre-commit-config.yaml` and running an `--all-files` pass.

## Common Commands

| Action           | Command                                               |
| ---------------- | ----------------------------------------------------- |
| Run API (dev)    | `uv run uvicorn main:app --reload`                    |
| New migration    | `uv run alembic revision --autogenerate -m "message"` |
| Apply migrations | `uv run alembic upgrade head`                         |
| Run tests        | `uv run -m pytest -q`                                 |

## Contributing

Issues & PRs welcome. Keep PRs focused; include tests and brief rationale.

## Roadmap (Condensed)

- OCR pipeline integration
- Document sharing & access controls
- Session rotation & pruning background task
- File storage (object store) for binary assets
- Expanded test coverage & CI

## License

MIT (proposed) – add LICENSE file if not present.

---

For backend implementation details see `backend/README.md`.
