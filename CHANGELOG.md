# Changelog — SpreadSheetz

All notable changes to this project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) with date‑stamped entries. Semantic versions are provisional during MVP.

## [Unreleased]

* Placeholder for upcoming changes.

## [0.1.0] — 2025-11-06

### Added

* **Docs:**

  * `docs/getting_started.md` — local‑first quickstart with Docker Postgres, Alembic, and victory test.
  * `docs/system_overview.md` — architecture, data flow, API surface, performance targets.
  * `docs/development_standards.md` — lint/format/test rules, DB and API standards, PR checklist.
  * `docs/security.md` — MVP controls + Phase 2 roadmap, checklists, and STRIDE snapshot.
  * `docs/knowledge_base.md` — sources table, recipes, API/SQL snippets.
  * `docs/ai_docs_organization_guide.md` — lean startup bundle; on‑demand references.
  * `AGENTS.md` — slim operating manual for Navigator/Specialists with handoff packet template.
  * `docs/checklists.md` — PR, ingestion, corrections, API, frontend, incident, and onboarding checklists.
  * `docs/glossary.md` — canonical terms (gap, provenance, natural key, etc.).

### Changed

* **Startup Context Model:** Trimmed cold‑start reading list for agents to: `README.md`, `project_charter.md`, `implementation_schedule.md`, `system_overview.md`, `development_standards.md`. Moved `getting_started.md`, `database_schema.md`, and `runbook.md` to **on‑demand**. (See `docs/ai_docs_organization_guide.md`.)
* **Security posture:** Clarified data classification and incident workflow; added vulnerability management cadence (`pip‑audit`, `npm audit`).

### Fixed

* **markdownlint:** Resolved MD033 (no‑inline‑HTML) and MD036 (emphasis as heading) in `docs/knowledge_base.md`.
* General heading spacing and single‑H1 compliance across new docs.

### Deprecated

* None.

### Removed

* None.

---

## [0.0.4] — 2025-11-05

### Changed

* Updated high‑level docs to align with new goals and two PDF references.
* Revised `README.md`, `docs/implementation_schedule.md`, `docs/project_charter.md`, `docs/project_brief.md`, `docs/database_schema.md`, and `docs/runbook.md` for MVP scope and terminology.

### Fixed

* Addressed various markdownlint warnings across existing docs.

---

## [0.0.3] — 2025-11-04

### Added

* Early `AI_GUIDE.md` front‑door doc.

### Fixed

* Markdown structure issues (MD022/MD032) in early agent docs.

---

## [0.0.2] — 2025-10-31

### Changed

* Iterated on AGENTS and Gemini startup docs to reduce token budgets.

---

## [0.0.1] — 2025-10-28

### Added

* Initial repository scaffolding and baseline documentation.

---

### Footnotes

* Dates are in **America/New_York** timezone.
* For incidents, see `docs/decisions/incident_*.md`.
* Security rotations (secrets/keys) are logged here without values.
