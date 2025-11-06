# Implementation Schedule — SpreadSheetz (v0.1)

**Scope:** 4-week MVP delivering a local-first app: curated WSP archive (2020–present), core stats, and “My Shows” loop with a minimal React UI. Guests/Teases, full backfill, and hosting are Phase 2.

**Status Legend:** ☐ Not Started · ▶ In Progress · ✅ Done · ⚠ Risk/Blocked

---

## Week 1 — Foundation

### Objectives

* Repo/CI setup, core data model, local Postgres, ingestion scaffold, foundational docs.

### Tasks

* ☐ Initialize repo structure (`src/`, `web/`, `alembic/`, `docs/`, `tests/`).
* ☐ Python toolchain: `uv`/`pip`, `ruff`, `pytest`, `pre-commit` hooks.
* ☐ CI stub: lint + tests on PR; CHANGELOG gate.
* ☐ DB: Postgres via Docker; SQLAlchemy models (Artist, Song, Venue, Show, Setlist; Users/Groups; user↔show join).
* ☐ Migrations: Alembic init + first migration.
* ☐ Ingestion scaffold: module layout + validators; 2020–present stubs.
* ☐ Docs: README, Brief, Charter; this Schedule; update Runbook and Security checklist skeletons.

### Deliverables

* Local environment working; `alembic upgrade head` succeeds.
* Models and first migration committed; CI green.

### Acceptance Criteria

* Can boot API with empty DB; health endpoint returns 200.
* Seed script inserts 1–2 example shows for manual UI testing.

### Week 1 Risks/NotesUI testing.

### Risks/Notes

* Decide on ID strategy (UUID vs int). Default: integer PK + unique natural keys for shows.

---

## Week 2 — Public Features

### Objectives

* Public read API, minimal React UI, first real import batch (200–500 shows).

### Tasks

* ☐ API routers: `/shows`, `/shows/{id}`, `/songs`, `/venues` (FastAPI + Pydantic models).
* ☐ Basic caching (per-route or simple in-process) for list endpoints.
* ☐ Frontend scaffold (Vite React): archive list, show detail, basic search/filter.
* ☐ Ingestion: implement 2020–present import path with provenance; error logging.
* ☐ Indexes: shows(date), setlist(show_id, position), song(title), venue(name, city).
* ☐ Docs: KB on sources + attribution; update Runbook with import steps.

### Deliverables

* Read-only archive accessible locally (API + UI).
* Imported 200–500 shows with provenance recorded.

### Acceptance Criteria

* `GET /shows` filters by year/city/venue; P95 < 2 s locally.
* Show detail includes ordered setlist, set/encore labels.

### Week 2 Risks/Notesore labels.

### Risks/Notes

* Source rate limiting → add polite delays + retry/backoff.

---

## Week 3 — Stats & “My Shows”

### Objectives

* Core stats endpoints, personal attendance loop, light admin for corrections.

### Tasks

* ☐ Stats service + endpoints: openers, gaps, debuts, most-seen songs/venues.
* ☐ Auth (local): session or JWT; Users/Groups; user↔show joins.
* ☐ “My Shows” UI: mark attendance, view personal stats.
* ☐ Admin (protected): submit/approve corrections; audit log table.
* ☐ Performance pass: verify essential indexes; simple caching for stats.
* ☐ Tests: unit (services), API integration (routers), ingestion fixtures.

### Deliverables

* End-to-end flow: mark attended shows → personal stats rendered.

### Acceptance Criteria

* `GET /stats/core` returns expected aggregates on sample dataset.
* User can add/remove attendance; changes reflected immediately.

### Week 3 Risks/Notesmmediately.

### Risks/Notes

* Stats correctness: add snapshot tests for a few known shows/years.

---

## Week 4 — Polish & Release v0.1

### Objectives

* UX polish, docs, security pass, CHANGELOG v0.1, demo script.

### Tasks

* ☐ Frontend: table accessibility, empty/loading states, mobile basics.
* ☐ Error handling & toasts; guardrails on admin actions.
* ☐ Security checklist: input validation review, rate limits on admin endpoints, secret management.
* ☐ Data backfill: add another era batch if time allows; spot-check vs sources.
* ☐ Docs: quickstart, FAQ, Runbook expansions, attribution section.
* ☐ Version: tag v0.1; write release notes.

### Deliverables

* Usable local app; docs current; v0.1 tagged.

### Acceptance Criteria

* README quickstart reproducible end-to-end on a clean machine.
* P95 < 2 s across core endpoints on local dataset.

### Week 4 Risks/Notesal dataset.

### Risks/Notes

* Defer advanced UI polish to Phase 2 to protect scope.

---

## Ongoing Backlog (Phase 2+)

* Guests & Teases entities + ingestion; jam flags, richer annotations.
* Full historical backfill with era-by-era QA.
* Deployment targets (Render/DO/other), HTTPS, observability.
* Precomputed aggregates for heavy stats; background jobs.
* Advanced search, tagging, setlist diffs, correction flows with history.

---

## RACI (Lightweight)

* **Owner (Connor):** Responsible/Accountable for scope, schema, merges, releases.
* **Contributor(s):** Support on ingestion, UI polish, tests.
* **Curator/Admin:** Approver for corrections; aligns source policy.

---

## Dependencies

* Python 3.11+, Node 18+, Docker for Postgres.
* Access to sources; respectful rate limits.

---

## Milestone Checklist

* ☐ M0: Repo/CI + first migration merged.
* ☐ M1: Archive read API + minimal UI; first 200–500 shows imported.
* ☐ M2: Stats + My Shows end-to-end; admin corrections.
* ☐ M3: v0.1 polish; docs + release notes; tag created.
