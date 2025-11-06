# Development Standards — SpreadSheetz (v0.1)

**Purpose.** Consistent, boring‑good engineering so we move fast without breaking data. This file defines code style, tests, migrations, docs, and Git workflow for the MVP.

**Read‑first order for contributors:** `README.md` → `docs/getting_started.md` → **this file** → `docs/runbook.md` → `docs/database_schema.md`.

---

## 1) Core Principles

* **Safety over cleverness.** Prefer readable, typed code with tests.
* **Idempotence by default.** Ingestion and migrations must be re‑runnable.
* **Single source of truth.** Schema + API contracts live in code + this repo; docs reflect code.
* **Small diffs.** Short‑lived branches; small PRs; fast review.

---

## 2) Tooling Matrix

* **Python**: 3.11+ (3.12 ok) · **Package**: `uv` (preferred) or `pip`
* **API**: FastAPI + Pydantic
* **DB**: Postgres 16 + Alembic
* **Testing**: `pytest`
* **Lint/Format**: `ruff` (format + lint)
* **Typing**: `mypy` (if enabled) or `pyright` (editor)
* **JS/TS (web)**: Node 18+, Vite/React · **Format/Lint**: Prettier + ESLint
* **Docs**: Markdown + markdownlint

> See project config files (`pyproject.toml`, `ruff.toml`, `.markdownlint.json`, etc.) for exact rules.

---

## 3) Repository Layout (MVP)

```
├─ src/spreadsheetz/
│  ├─ api/                 # FastAPI routers, deps, schemas
│  ├─ ingestion/           # CLI entrypoints, adapters, normalization
│  ├─ db/                  # models, queries, alembic helpers
│  ├─ services/            # domain logic (stats, attendance)
│  └─ util/                # small, shared utils (pure functions)
├─ scripts/                # one‑off admin or seed scripts
├─ alembic/                # migrations
├─ web/                    # minimal React UI (vite)
├─ tests/                  # pytest (mirrors src structure)
└─ docs/                   # you are here
```

---

## 4) Python Standards

### 4.1 Style & Lint

* Use **ruff** for both formatting and linting.
* Keep functions small (≤ 50 lines as a guideline). Extract pure helpers.
* Prefer dataclasses/Pydantic models to loose dicts.
* Avoid side effects in module import time.

**Commands**

```bash
uv run ruff format .
uv run ruff check .
```

### 4.2 Typing

* All public functions must be type‑annotated; APIs use Pydantic models.
* `from __future__ import annotations` where helpful.
* If `mypy` is enabled:

  ```bash
  uv run mypy src tests
  ```

### 4.3 Tests

* Unit tests for pure logic; integration tests for API/DB.
* Naming: `tests/<area>/test_<module>.py`.
* Use factories/builders for fixtures; avoid test order coupling.

**Commands**

```bash
uv run pytest -q
```

Coverage targets (guideline): overall ≥ 70%; critical modules ≥ 85%.

---

## 5) API Standards (FastAPI)

* Schemas live under `src/spreadsheetz/api/schemas.py` (or per‑router schemas).
* Pagination: `page`, `per_page` (or cursor if needed); default `per_page=50`.
* Validation: strict Pydantic models; reject ambiguous inputs.
* Versioning strategy: route groups by capability changes if needed (e.g., `/v1`).
* Error shape:

  ```json
  {"error": {"code": "<slug>", "message": "<human>"}}
  ```
* Logging: one structured line per request (method, path, status, ms).

---

## 6) Database Standards (Postgres + Alembic)

### 6.1 Modeling

* Prefer **natural keys** for dedupe (e.g., `(artist_id, date, venue_id)`) with a surrogate `id` for joins.
* Enforce **NOT NULL** and **CHECK** constraints for invariants (e.g., set positions ≥ 1 and contiguous per show).
* Index hot filters: `(artist_id, date)`, `(show_id, position)`.

### 6.2 Migrations

* One feature = one migration; use deterministic naming: `YYYYMMDDHHMM_<slug>.py`.
* Never edit applied migrations. Create a new migration for changes.
* Include **data backfills** in migrations only if required for invariants; otherwise script in `scripts/`.

**Commands**

```bash
alembic revision -m "add correction_log table"
alembic upgrade head
```

### 6.3 SQL Style

* Keep complex queries in `.sql` files or dedicated query modules; unit test them.
* Prefer explicit column lists over `SELECT *` in application code.

---

## 7) Ingestion Standards

* **Idempotent upserts** keyed by natural keys; never insert duplicates.
* **Provenance** is mandatory: `source`, `source_ref`, `ingested_at` stored alongside rows.
* **Retries & Logging**: retry transient failures with backoff; log attempt count and error.
* **Normalization**: canonicalize song titles; track aliases separately.
* **Dry‑run** mode for all destructive operations.

CLI example:

```bash
python -m src.spreadsheetz.ingestion.cli import-year --year 2024 --dry-run
```

---

## 8) Frontend Standards (Minimal UI)

* Keep UI components simple; fetch via typed client where possible.
* Prettier on save; ESLint no‑unused‑vars.
* Accessibility baseline: semantic elements; focus management on route change.

**Commands**

```bash
npm run lint
npm run format
```

---

## 9) Documentation Standards

* Every PR updates relevant docs (README, schema notes, runbook snippets).
* Markdown must pass **markdownlint** (avoid duplicate headings MD024, etc.).
* Keep code blocks copy‑pasteable; prefer short sections with links out.

**Commands**

```bash
npx markdownlint-cli2 "**/*.md"
```

---

## 10) Git Workflow

* **Branching**: `feature/<slug>`, `fix/<slug>`, `chore/<slug>`.
* **Commit messages**: Conventional Commits (subset):

  * `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `perf:`
  * Scope optional, e.g., `feat(api): add /version`
* **PR size**: aim for < 400 lines diff; split if larger.
* **Reviews**: at least 1 reviewer; respond to all comments or file a follow‑up issue.

---

## 11) CI Expectations (baseline)

Each PR should pass:

* `ruff format` (no changes) and `ruff check` (no errors)
* `pytest` (green)
* `markdownlint` (clean)
* (Optional) `mypy` clean when enabled

Example local pre‑flight:

```bash
uv run ruff format . && uv run ruff check .
uv run pytest -q
npx markdownlint-cli2 "**/*.md"
```

---

## 12) Secrets, Config, and Environments

* **Never** commit secrets; `.env` at repo root is git‑ignored.
* Config via env vars; document defaults in `README.md`.
* Local dev: `.env` → `DATABASE_URL`, `APP_ENV`, `SECRET_KEY`.

---

## 13) Data Quality & Corrections

* Enforce uniqueness and contiguity constraints in DB + tests.
* All curator‑applied changes log to `correction_log` with `reason`, `source`, `reviewer`, and timestamps.
* Do not overwrite provenance; append and audit.

---

## 14) Performance Budgets (Dev targets)

* `/shows` list: < 400ms p95 on dev machine.
* Yearly ingest per band: < 5 minutes.
* Core stats: < 2s per artist/year query with indexes.

Track regressions in PR descriptions if exceeded.

---

## 15) Exceptions & RFCs

* If you must break a rule, add an **Exceptions** note in the PR with rationale and follow‑up.
* Design changes that impact schemas or public API require a short **RFC** (`docs/decisions/<date>_<slug>.md`).

---

## 16) Development Checklists

### 16.1 Pull Request (Definition of Done)

* [ ] Small, focused diff; linked to a schedule task
* [ ] Tests added/updated; `pytest` green
* [ ] `ruff format` + `ruff check` clean
* [ ] Docs updated (README/runbook/schema/KB as needed)
* [ ] Migrations included (if schema changed)
* [ ] Manual smoke test steps noted in PR

**Local pre‑flight**

```bash
uv run ruff format . && uv run ruff check .
uv run pytest -q
npx markdownlint-cli2 "**/*.md"
```

### 16.2 Data Model Change

* [ ] Design constraints (NOT NULL, UNIQUE, CHECKs, FKs)
* [ ] Write Alembic migration with deterministic name
* [ ] Backfill/data migration if required (or script under `scripts/`)
* [ ] Update `docs/database_schema.md`
* [ ] Add/update tests; run `pytest`

**Commands**

```bash
alembic revision -m "add correction_log table"
alembic upgrade head
```

### 16.3 API Endpoint Addition

* [ ] Define request/response schemas (Pydantic)
* [ ] Validate inputs; enforce pagination caps
* [ ] Add tests (unit + integration)
* [ ] Add route to docs (KB snippet if useful)
* [ ] Log one structured line per request

### 16.4 Frontend Feature (Minimal UI)

* [ ] Simple, accessible markup; no `dangerouslySetInnerHTML`
* [ ] Data fetched via typed client; handle loading/error states
* [ ] Prettier/ESLint clean
* [ ] Include a basic screen reader check

---

## 17) Lint Trap Map

* **MD024**: avoid duplicate headings; qualify titles
* **MD033**: no inline HTML; use Markdown
* **MD036**: turn bold pseudo‑headings into real headings

---

**Keep it boring. Ship small. Measure.**
