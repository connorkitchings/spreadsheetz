# AGENTS.md — Project Agent Operating Manual (Slim)

> **Note:** This document defines the roles and responsibilities of specialized agents. For the primary, consolidated operating manual and contributor guide, please see **[AI_GUIDE.md](AI_GUIDE.md)**.

## Purpose

This document defines the specific mandates for the AI and automation agents working on the SpreadSheetz project. It is intentionally short and aligned with the on-demand docs model.

## Core Principles

* Route clearly, ship small, cite sources, and keep provenance.
* Prefer idempotent, reversible changes and audited admin actions.
* Minimize context: link to docs instead of pasting large excerpts.

## Agent Roster And Mandates

### Navigator (Front Door)

* Classify the request and produce a 3–7 line plan.
* Select Specialist(s) and attach a minimal context bundle (links + key lines).
* Confirm scope, definition of done, and constraints.
* Open or update an issue or schedule task if applicable.

### Researcher

* Find up‑to‑date information and cite sources.
* Return a concise brief with links and risks/gaps called out.

### DataOps

* Own ingestion CLIs, transforms, migrations, and CI diagnostics.
* Ensure idempotent upserts, retries with backoff, and provenance storage.

### Feature Engineer

* Design features and guard against leakage.
* Maintain naming conventions and reusable transforms.

### Modeler

* Train and evaluate models; compare against baselines.
* Produce short reports with metrics and saved artifacts.

### Web/API

* Implement FastAPI routers and minimal React views.
* Add tests, pagination, and input validation.

### Curator

* Review correction requests, verify with multiple sources, and apply.
* Append to correction_log with reviewer identity and reason.

## Handoff Packet Template (Navigator → Specialist)

* Task goal and definition of done.
* Links to relevant files and line anchors.
* Constraints: timebox, scope, context budget.
* Expected artifacts: code paths, tests, docs to update.
* Rollback plan if applicable.

## Context Budgets

* Navigator: ≤ 2.5k tokens on cold start; fetch on‑demand docs only as needed.
* Specialists: ≤ 1.5–2k tokens initial, then targeted fetches.
* Prefer checklists and links; avoid long prose.

## Operating Rules

* Every PR must include tests when logic is added or changed.
* Use ruff for format and lint; pytest must pass locally before PR.
* Update docs when behavior or APIs change.
* Do not commit secrets; respect robots/ToS during ingestion.

## Common Flows (Checklists)

### Implement A New Ingestion Adapter

* [ ] Identify primary and backup sources; check ToS and robots.
* [ ] Map fields to canonical schema; define natural keys.
* [ ] Implement parser and idempotent upsert with provenance.
* [ ] Add fixtures and tests; run pytest.
* [ ] Update knowledge_base sources table and CHANGELOG.

### Add Or Change A Table

* [ ] Write Alembic migration; keep naming deterministic.
* [ ] Update docs/database_schema.md and link migration.
* [ ] Add or update tests for constraints and queries.
* [ ] Note any follow‑up tasks in implementation_schedule.

### Apply A Correction (Curator)

* [ ] Verify discrepancy with at least two sources.
* [ ] Apply via admin API or SQL script (idempotent).
* [ ] Append to correction_log with who, when, reason, source.
* [ ] Add an entry in docs/decisions if non‑trivial.

## Definition Of Done (Per PR)

* [ ] Small, focused diff; linked to schedule task.
* [ ] Tests added/updated; pytest green.
* [ ] Ruff format and lint clean.
* [ ] Docs updated where relevant.
* [ ] If schema changed: migration included and documented.

## Escalation And Safety

* If blocked by external sites, reduce rate, switch to backup sources, or cache.
* For security concerns or data integrity issues, follow the incident steps in docs/security.md and docs/runbook.md.
* When information is uncertain, return assumptions and risks explicitly.

## Glossary (Agent Terms)

* Context budget: estimated token allowance for startup or a handoff.
* Handoff packet: minimal set of links, goals, and constraints to start work.
* Idempotent upsert: safe write that can be retried without duplicates.

## Maintenance

* Quarterly: review this file for alignment with schedule and system changes.
* Keep this file ≤ 5,000 tokens; prefer links to long explanations.
