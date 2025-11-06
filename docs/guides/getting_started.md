# Getting Started — SpreadSheetz (v0.1)

> **Goal:** get a local dev environment running (API + DB + minimal web) in minutes, with a short “victory test” to prove the loop works. For deeper operations, see `docs/runbook.md`.

* **What you’ll get:** FastAPI at `http://localhost:8000/docs`, a Postgres DB, and a minimal React UI at `http://localhost:5173`.
* **What this doc is not:** full architecture or policies — those live in `README.md`, `docs/project_charter.md`, and `docs/database_schema.md`.

---

## TL;DR (5 steps)

1. Clone & create a virtual env
2. Start Postgres in Docker
3. Add `.env` and run Alembic migrations
4. Install deps; run API
5. Start the minimal web UI & verify

---

## Prerequisites

* **Python** ≥ 3.11 (3.12+ ok)
* **Node** ≥ 18 (for the minimal web)
* **Docker** (for local Postgres)
* **uv** (preferred) or `pip`
* **Git**

> Tip: This repo uses `ruff`, `pytest`, and `alembic` (installed via Python deps). See `README.md` for the broader toolchain.

---

## 1) Clone the repo & set up your environment

```bash
# Clone
git clone <your-repo-url> spreadsheetz
cd spreadsheetz

# Create & activate a virtual env (uv)
uv venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

# Install Python deps (choose one)
uv pip install -r requirements.txt
# or, if using pyproject
# uv pip install -e .
```

> Alternative with `pip` (if you don’t want uv):
>
> ```bash
> python -m venv .venv
> source .venv/bin/activate
> pip install -r requirements.txt
> ```

---

## 2) Start local Postgres (Docker)

```bash
docker run --name spreadsheetz-pg \
  -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=spreadsheetz \
  -p 5432:5432 -d postgres:16
```

> You can use a local Postgres instead; just make sure your `DATABASE_URL` matches.

---

## 3) Configure environment variables (`.env`)

Create `.env` in the repo root:

```dotenv
# Database
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/spreadsheetz

# App
APP_ENV=dev
SECRET_KEY=change-me
```

> Never commit `.env`. There’s a `.env.example` for reference if provided.

---

## 4) Initialize the database (Alembic)

```bash
# Apply all migrations
alembic upgrade head

# (Optional) Seed a couple of rows for dev smoke tests
python scripts/seed_minimal_data.py
```

Troubleshooting? See **Runbook → Database Lifecycle**.

---

## 5) Run the API (FastAPI/Uvicorn)

```bash
uvicorn src.spreadsheetz.api.main:app --reload --port 8000
# Visit http://localhost:8000/docs for Swagger UI
```

Expected:

* `GET /health` returns 200
* `GET /shows` returns empty or your seeded rows

---

## 6) Run the minimal web UI

```bash
cd web
npm install
npm run dev
# Visit http://localhost:5173
```

Expect to see a basic archive list/detail view. If the page can fetch from the API, your loop is good to go.

---

## 7) Victory Test (prompt → PR)

Use this to validate the full toolchain — adapted from `AGENTS.md`:

1. Add a trivial API change (e.g., a `/version` endpoint returning `v0.1.0`).
2. Write a tiny test that asserts the response schema/value.
3. Run checks:

   ```bash
   uv run ruff format . && uv run ruff check .
   uv run pytest -q
   ```

4. Commit on a branch and open a PR:

   ```bash
   git checkout -b feature/add-version-endpoint
   git commit -am "feat(api): add /version endpoint [schedule:week1]"
   git push origin feature/add-version-endpoint
   ```

Success = PR passes CI and merges. You’re ready for real tasks.

---

## 8) Ingestion quick start (Phase 1 focus: 2020–present)

The MVP imports recent years first (2020→present) with provenance, then backfills. Example (subject to your CLI wiring):

```bash
# Dry-run an import for 2023
python -m src.spreadsheetz.ingestion.cli import-year --year 2023 --dry-run

# Commit an import with logging & upsert semantics
python -m src.spreadsheetz.ingestion.cli import-year --year 2024 --commit --upsert --log logs/ingest_2024.log
```

Minimum validation rules (see `docs/runbook.md`):

* Unique `(artist_id, date, venue_id)` for `show`
* `setlist.position` is contiguous per show (1-based)
* Normalize song titles; store `source`, `source_ref`, `ingested_at`

---

## 9) Personal stats (“My Shows”) — MVP wiring

* Minimal local auth (session/JWT) to mark attendance
* Endpoints (subject to change):

  * `GET /me/shows` — list attended shows
  * `GET /me/stats` — personal stats
* UI: a simple toggle to mark/unmark attendance on show pages

> Personal stats reuse the same core stats engine with a user filter — the **killer feature** that drives engagement.

---

## 10) Corrections & curation (light admin)

We follow a **curated, source‑of‑truth** model:

* Intake via a simple email/form (MVP)
* Curator verifies against ≥2 sources
* Apply via protected admin API or SQL script
* Record in `correction_log` (see `docs/runbook.md` §5)

> Attribution & ethics: credit sources in UI/docs; avoid republishing long‑form content verbatim.

---

## 11) Troubleshooting

When in doubt, open **`docs/runbook.md`**. Common fixes:

* **DB connection refused** → Docker running? Port 5432 free? `DATABASE_URL` correct?
* **Alembic heads conflict** → `alembic heads` → `alembic merge -m "merge heads" <head1> <head2>`
* **Duplicate shows** → ensure natural key uniqueness; use `--upsert`
* **Slow `/stats/core`** → check indexes; enable simple caching (see Runbook)

---

## 12) Next steps

* Pick a Week/Task from `docs/implementation_schedule.md`
* For schema/API work, read `docs/database_schema.md` first
* Keep `CHANGELOG.md` updated; follow `docs/development_standards.md`

---

## 13) Uninstall/reset (local)

```bash
# Stop & remove DB container (destructive)
docker rm -f spreadsheetz-pg

# Remove virtual env
deactivate 2>/dev/null || true
rm -rf .venv
```

---

### Links

* Front door: `README.md`
* Charter & brief: `docs/project_charter.md`, `docs/project_brief.md`
* Schedule: `docs/implementation_schedule.md`
* Schema: `docs/database_schema.md`
* Runbook: `docs/runbook.md`
* Security: `docs/security.md`
