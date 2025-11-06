# Project Charter & Brief — SpreadSheetz (v0.1)

A lean, source‑attributed setlist archive and personal attendance tracker for jam‑band fans, starting with Widespread Panic and expanding to Goose, Phish, Billy Strings, Umphrey’s McGee, and Eggy. MVP focuses on reliable ingestion (2020–present), core stats, and “My Shows,” with a lightweight corrections workflow.

---

## Problem and Opportunity

Fan setlist data is scattered, inconsistently formatted, and occasionally contradictory. Existing sites excel at historical archives but often lack transparent provenance, simple personal stats, or an easy corrections workflow. There is an opportunity to provide a clean, auditable data spine with fast core stats and a compelling personal overlay.

---

## Target Users and Primary Jobs

* Enthusiasts who want a fast, trustworthy archive with gap/frequency stats.
* Attendees who want to mark shows and view personalized stats.
* Curators who want a light process to propose and apply corrections with provenance.

---

## Objectives (MVP)

* Ingest and normalize 2020–present shows for the initial band list.
* Provide core stats: frequency, gaps, streaks, openers/closers.
* Support personal attendance toggles and personal overlays of core stats.
* Store provenance and expose a curator corrections flow with an auditable log.
* Ship a minimal, usable web UI backed by a typed API and Postgres schema.

---

## Non‑Goals (MVP)

* Rich editorial content, reviews, or long‑form media hosting.
* Full RBAC or public write APIs.
* Advanced recommendation engines or machine‑learning predictions.

---

## MVP Feature List

* Multi‑source ingestion with idempotent upserts and provenance fields.
* Core schema for artist, venue, show, set, song, set_song, attendance, and correction_log.
* FastAPI endpoints for browsing shows, fetching details, and retrieving core stats.
* Minimal React UI: archive filters, show page with sets and attendance toggle, stats views.
* Light admin: apply corrections and record deltas in correction_log.

---

## Data and Sources

* Maintain a per‑band table of primary and backup sources in `docs/knowledge_base.md`.
* Store `source`, `source_ref`, and `ingested_at` for all ingested entities.
* Require at least two corroborating sources for contentious changes.

---

## Architecture Snapshot

* Frontend: Vite/React minimal UI.
* API: FastAPI with Pydantic models, pagination, and input validation.
* Database: Postgres 16 with Alembic migrations; indexes on natural keys and hot paths.
* Ingestion: CLI entrypoints, retries with backoff, idempotent upserts, structured logs.

See `docs/system_overview.md` for the broader map.

---

## Success Metrics

Leading indicators:

* Time to first successful local run under thirty minutes using `getting_started.md`.
* Ingest success rate over ninety‑eight percent per band per run.
* P95 latency under four hundred milliseconds for common show list queries.

Lagging indicators:

* Number of unique users marking attendance.
* Ratio of curated corrections accepted versus submitted.
* Return visits to personal stats pages.

---

## Milestones (Snapshot)

* Week 1: Local dev loop, DB bootstrapped, core schema and initial ingest adapter.
* Week 2: API browse/detail endpoints, basic stats service, minimal UI list/detail.
* Week 3: Personal attendance toggles, personal stats overlay, provenance polish.
* Week 4: Corrections flow (admin), data checks, performance tuning, docs pass.

See `docs/implementation_schedule.md` for current status and task owners.

---

## Risks and Mitigations

* Source blocking or drift: polite rate limits, rotating agents, backup sources, cached fetches.
* Canonicalization disagreements: alias tables, documented rules, curator approvals.
* Data quality regressions: natural key constraints, transform tests, correction_log audits.

---

## Constraints and Assumptions

* Local‑first development environment using Docker Postgres.
* Minimal auth for attendance in MVP; OAuth in a later phase.
* No storage of passwords; only provider IDs and email when auth is enabled.

---

## Dependencies

* Python 3.11 or newer, Node 18 or newer, Docker, uv or pip, Postgres 16.
* markdownlint, ruff, pytest, Alembic for developer workflow quality.

---

## Acceptance Criteria for MVP

* Ingestion runs idempotently for 2020–present across initial bands with provenance.
* Browse and detail endpoints return correct, paginated results with tests.
* Stats endpoints deliver frequency and gap metrics within stated performance targets.
* Users can mark attendance and see personal overlays of core stats.
* Curators can apply corrections, and each change is recorded in correction_log.

---

## References

* System: `docs/system_overview.md`
* Schema: `docs/database_schema.md`
* Standards: `docs/development_standards.md`
* Security: `docs/security.md`
* Sources and recipes: `docs/knowledge_base.md`
* Getting started: `docs/getting_started.md`

---
---

Authorizes and frames the SpreadSheetz project. This charter defines scope, objectives,
roles, constraints, success criteria, and governance. It is intentionally short and
aligned with the lean startup bundle.

---

## 1) Purpose and Vision

Deliver a lean, source‑attributed setlist archive and personal attendance tracker for
jam‑band fans. The MVP emphasizes reliable ingestion for recent years, fast core stats,
and a lightweight corrections workflow that preserves provenance.

---

## 2) Scope

### In Scope (MVP)

* Bands: Widespread Panic
* Time window: 2020 to present prioritized, then backfill.
* Capabilities: ingestion with provenance, core stats (frequency, gaps, streaks,
openers/closers), "My Shows" attendance, curator corrections, minimal web UI, typed API.

### Out of Scope (MVP)

* Rich editorial content or public write APIs.
* Full RBAC or complex auth flows.
* ML recommendations or predictions.

---

## 3) Objectives and Success Criteria

* Ingest and normalize shows for 2020–present across initial bands with idempotent
upserts and provenance.
* Serve core stats within stated performance targets.
* Support personal attendance and personal stat overlays.
* Enable curator corrections with an auditable log.

**KPIs**

* Time to first local run under thirty minutes.
* Ingest success rate ≥ ninety‑eight percent per run.
* `/shows` list p95 latency < four hundred milliseconds on dev hardware.
* Engagement: users marking attendance and revisiting personal stats pages.

---

## 4) Stakeholders and Roles

* **Product Owner**: sets priorities and accepts scope.
* **Tech Lead**: architecture, code review, performance targets.
* **Curator**: validates corrections and applies changes with provenance.
* **Navigator (Agent)**: triages requests and assembles minimal context bundles.
* **Specialists (Agents)**: Researcher, DataOps, Feature Engineer, Modeler, Web/API.

See `AGENTS.md` for handoffs and context budgets.

---

## 5) Constraints and Assumptions

* Local‑first development using Docker Postgres.
* Minimal auth in MVP; OAuth in a later phase if needed.
* No password storage; email and provider ID only when auth is enabled.
* Respect robots and terms of service for sources; polite ingestion.

---

## 6) Deliverables

* Postgres schema with migrations.
* Ingestion CLIs per band with provenance fields.
* FastAPI endpoints for browse, detail, and core stats.
* Minimal React UI for archive and "My Shows".
* Documentation: system overview, getting started, development standards, knowledge
base, security, checklists, changelog.

---

## 7) High‑Level Plan and Milestones

* **Week 1**: Local loop, schema, first ingest adapter, health checks.
* **Week 2**: Browse/detail endpoints, basic stats, minimal UI list/detail.
* **Week 3**: Attendance toggles, personal stats overlay, provenance polish.
* **Week 4**: Corrections flow, data checks, perf tuning, docs pass.

See `docs/implementation_schedule.md` for task owners and current status.

---

## 8) Risks and Mitigations

* **Source blocking or drift**: rate limiting, retries, alternate sources, caching.
* **Canonicalization disputes**: alias tables, documented rules, curator approvals.
* **Data integrity regressions**: constraints, tests, correction log audits.
* **Performance regressions**: indexes, query reviews, budgets tracked in PRs.

---

## 9) Governance and Change Control

* Changes to schema or public API require a short RFC under `docs/decisions/` and
review by Product Owner and Tech Lead.
* All user‑visible changes logged in `CHANGELOG.md`.
* Security incidents follow procedures in `docs/security.md` and `docs/runbook.md`.

---

## 10) Acceptance and Review

* MVP accepted when success criteria in Section 3 are met and milestones in Section 7
are completed.
* This charter is reviewed at the end of each milestone and updated as needed.

---

## 11) References

* System Overview: `docs/system_overview.md`
* Development Standards: `docs/development_standards.md`
* Security: `docs/security.md`
* Knowledge Base: `docs/knowledge_base.md`
* Getting Started: `docs/getting_started.md`
* Implementation Schedule: `docs/implementation_schedule.md`
