# Runbook — SpreadSheetz (v0.1)

> Operator’s guide for local development, data ingestion, troubleshooting, and common playbooks.

---

## 1. Environment Bootstrap

### 1.1 Prerequisites

* Python 3.11+
* Node 18+
* Docker (for Postgres)
* `uv` (or `pip`), `ruff`, `pytest`, `alembic`, `uvicorn`

### 1.2 Clone & Create Env

```bash
git clone <repo> spreadsheetz
cd spreadsheetz
uv venv && uv pip install -r requirements.txt
# or pip/venv alternative
```

### 1.3 Configure .env

Create `.env` at repo root:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/spreadsheetz
APP_ENV=dev
SECRET_KEY=change-me
```

---

## 2. Database Lifecycle

### 2.1 Start Local Postgres

```bash
docker run --name spreadsheetz-pg \
  -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=spreadsheetz \
  -p 5432:5432 -d postgres:16
```

### 2.2 Apply Migrations

```bash
alembic upgrade head
```

### 2.3 Create Seed Data (Optional)

```bash
python scripts/seed_minimal_data.py
```

### 2.4 Reset Database (Destructive)

```bash
docker rm -f spreadsheetz-pg
# re-run Section 2.1 then alembic upgrade head
```

---

## 3. Application Lifecycle

### 3.1 Run API

```bash
uvicorn src.spreadsheetz.api.app:app --reload --port 8000
# Swagger: http://localhost:8000/docs
```

### 3.2 Run Web Frontend

```bash
cd web
npm install
npm run dev
# http://localhost:5173
```

### 3.3 Smoke Test Checklist

* API `GET /health` returns 200
* `GET /shows` returns empty or seeded data
* Frontend loads archive list page without errors

---

## 4. Ingestion & Data Ops

### 4.1 Ingestion Targets (Phase 1)

* Era: **2020–present**
* Sources: Everyday Companion, PanicStream, TourWrangler; setlist.fm for verification

### 4.2 Ingestion Commands (Examples)

```bash
# dry-run recent year import
python -m src.spreadsheetz.ingestion.cli import-year --year 2023 --dry-run

# execute a year import with logging and provenance
python -m src.spreadsheetz.ingestion.cli import-year --year 2023 --commit --log logs/ingest_2023.log

# re-run idempotently to upsert (no duplicate rows)
python -m src.spreadsheetz.ingestion.cli import-year --year 2024 --commit --upsert
```

### 4.3 Provenance Policy

* Store `source`, `source_ref`, `ingested_at` on `show` rows
* Keep raw fetch artifacts in `data/raw/<source>/<yyyy>/` for reproducibility
* Never overwrite raw files; write new timestamped files

### 4.4 Validation Rules (Minimum)

* Unique `(artist_id, date, venue_id)` for `show`
* `setlist.position` is 1-based contiguous per `show`
* Song titles normalized (trim, canonical capitalization)

---

## 5. Admin & Corrections (Light)

### 5.1 Intake Flow

* Users submit correction via (temporary) email or form
* Curator verifies against at least **two** sources
* Curator applies edit via admin API or SQL script with comment

### 5.2 Audit Log (Minimum)

* Table `correction_log` (Phase 1 simple): `id, entity, entity_id, field, old_value, new_value, source_refs, curator, created_at`

---

## 6. Testing & QA

### 6.1 Commands

```bash
ruff check . && ruff format --check .
pytest -q
```

### 6.2 Must‑Pass Tests (Phase 1)

* Service: opener detection, debut extraction, most‑seen aggregates
* API: `/shows`, `/shows/{id}`, `/stats/core` return expected schemas
* Ingestion: sample fixture import idempotent (no dupes)

### 6.3 Data Spot‑Checks

* Random 10 shows/era vs sources; record notes in `docs/qa/spotchecks.md`

---

## 7. Observability (Local)

### 7.1 Logging

* API logs: console DEBUG in dev
* Ingestion logs: write to `logs/ingest_*.log`

### 7.2 Performance Checks

* Verify indexes: `EXPLAIN ANALYZE` on heavy stats queries
* Target P95 < 2s locally on `/shows` and `/stats/core`

---

## 8. Backup & Restore (Local)

### 8.1 Snapshot Backup

```bash
pg_dump --format=custom --dbname=postgresql://postgres:postgres@localhost:5432/spreadsheetz \
  --file=backups/spreadsheetz_$(date +%Y%m%d_%H%M).dump
```

### 8.2 Restore Snapshot

```bash
pg_restore --clean --if-exists --dbname=postgresql://postgres:postgres@localhost:5432/spreadsheetz \
  backups/<file>.dump
```

---

## 9. Release Flow (Local Tags)

### 9.1 Version Bump

* Update `CHANGELOG.md`
* Commit: `docs: prepare v0.1` (example)

### 9.2 Tag

```bash
git tag v0.1.0 -m "SpreadSheetz v0.1.0"
git push origin v0.1.0
```

---

## 10. Common Errors & Fixes

### 10.1 Connection Refused (DB)

* Ensure Docker is running and container `spreadsheetz-pg` is healthy
* Confirm `DATABASE_URL` matches container port (5432)

### 10.2 Alembic Heads Conflict

```bash
alembic heads
# identify branches, then
alembic merge -m "merge heads" <head1> <head2>
```

### 10.3 Duplicate Shows on Re‑Import

* Ensure natural key uniqueness on `(artist_id, date, venue_id)`
* Use `--upsert` in ingestion CLI

### 10.4 Slow `/stats/core`

* Add/verify indexes (see schema doc)
* Consider caching layer (simple in‑process) for expensive aggregations

---

## 11. Operator Checklists

### 11.1 Daily Dev Checklist (When Working on Data)

* Pull latest, run tests
* Run ingestion for most recent shows if needed
* Spot‑check one random show in UI vs sources

### 11.2 Pre‑Merge Checklist

* Lint & tests green
* Alembic migration present for schema changes
* Docs updated (README/Runbook/Schema/CHANGELOG)

---

## 12. Contacts & Ownership

* **Owner:** Connor Kitchings (`connorkitchings`)
* **Curator (internal role):** same as owner for MVP

---

## 13. Future Enhancements

* Promote `correction_log` to full admin UI with diff previews
* Add materialized views for heavy stats
* Introduce UUIDv7 and soft‑delete for auditability
* Schedules & background jobs for nightly refresh (Phase 2)

---

## 14) Operational Checklists

### 14.1 Ingestion Run (Year/Band)

* [ ] Dry‑run first with logs
* [ ] Check natural key uniqueness
* [ ] Use idempotent upsert flags
* [ ] Verify provenance fields set (`source`, `source_ref`, `ingested_at`)
* [ ] Capture run logs and summary counts

**Example**

```bash
python -m src.spreadsheetz.ingestion.cli import-year \
  --band wsp --year 2024 --dry-run --log logs/wsp_2024_dryrun.log
# Commit
python -m src.spreadsheetz.ingestion.cli import-year \
  --band wsp --year 2024 --commit --upsert --log logs/wsp_2024_commit.log
```

### 14.2 Observability & Quality

* [ ] Structured logs for ingest/API (JSON lines)
* [ ] Add counters/timers for slow paths
* [ ] Verify dedupe ratio and ingest success rates
* [ ] Add a smoke test or health check if missing

### 14.3 Release Prep (Phase 2+)

* [ ] Secrets in managed store; rotate if due
* [ ] CORS configured to known origins
* [ ] Rate limiting enabled
* [ ] Backups configured; restore drill documented
* [ ] CSP headers set for UI

### 14.4 Incident Response (Lightweight)

* [ ] Detect: identify spike/error via logs/metrics
* [ ] Stabilize: throttle or disable affected endpoints
* [ ] Triage: scope blast radius; collect request IDs and time window
* [ ] Fix: patch and add a regression test
* [ ] Report: write `docs/decisions/incident_<YYYYMMDD>_<slug>.md`
* [ ] Prevent: add guardrail (constraint/test/lint)

### 14.5 Backup/Restore Drill (Phase 2+)

* [ ] Document backup cadence and retention
* [ ] Perform a restore to a scratch DB
* [ ] Validate counts and key constraints
* [ ] Record steps, duration, and issues in runbook
