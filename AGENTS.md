# AGENTS.md — Project Agent Operating Manual (Slim)

> **Purpose:** This file is the **constitution** for AI coding agents (Claude Code, GPT-5, Cursor, etc.). It defines how to work in this repo, what is in-bounds vs. gated by humans, and the routing rules between agent roles. Keep this file short and link out to deeper docs when needed.

**AI_GUIDE.md vs AGENTS.md:**

- **AI_GUIDE.md** → How to do work (playbooks, commands, context lookup)
- **AGENTS.md** → Rules of engagement (guardrails, roles, escalation, quality gates)
- Read AI_GUIDE first for "how", then AGENTS for "governance"

**Read-First:** `AI_GUIDE.md` → `docs/template_starting_guide.md` (when converting from template) → `docs/project_charter.md` → `docs/implementation_schedule.md` → `docs/development_standards.md` → `docs/checklists.md` → `docs/ai_session_templates.md`

**Status Legend:** ☐ Not Started · ▶ In Progress · ✅ Done · ⚠ Risk/Blocked

**Last Updated:** 2025-11-04

---

## 1) Core Guardrails (Do / Don't)

### Do

- Start/End every session with the templates in `docs/ai_session_templates.md` and log to `session_logs/`.
- When adopting this repo for a new project, run through `docs/template_starting_guide.md` before committing code.
- Keep changes **small and testable**; 1 schedule task = 1 PR.
- Run `uv sync` (first time), then `uv run ruff format . && uv run ruff check . && uv run pytest` before pushing.
- Treat CLI/script output as next-step prompts; follow suggested commands.
- Update docs when behavior changes (Charter, KB, or architecture notes).

### Don't (without human review)

- Secrets/credentials, auth/security config, schema/API contracts, DB migrations, deployment/infrastructure, or dependency upgrades beyond patch. Open a planning task instead and request review. See **Escalation Triggers** below.

---

## 2) Roles & Mandates

Use these lightweight "hats" to structure tasks. For solo projects, wear multiple hats but keep scopes separate.

- **Navigator (Front Door):** Classify request, outline 3–7 line plan, route to a hat, ensure a clear demo-able outcome.
  - *Deliverable:* Plan doc or session log with routing decision

- **Researcher:** Gather current facts, APIs, library usage; summarize in log with links.
  - *Deliverable:* Research summary in session log or KB entry

- **DataOps:** Ingestion, schemas, validation, observability; ensure reproducible runs.
  - *Deliverable:* Working pipeline + data quality tests

- **Feature Engineer / Core Logic:** Transform data or implement core business logic with tests.
  - *Deliverable:* Module with unit tests, ≥80% coverage

- **Modeler (if applicable):** Baselines → metrics → model/logic card; compare to naive/previous.
  - *Deliverable:* Model card + comparison report

- **App/UI:** Minimal CLI/UI surfaces; wire happy-path first.
  - *Deliverable:* Working demo (screenshots/video)

- **DevEx/CI:** Tests, linting, CI jobs, release tagging, monitoring hooks.
  - *Deliverable:* Green CI run or new automation

- **Docs/PM:** Thread decisions into Charter/KB; keep schedule and checklists aligned.
  - *Deliverable:* Updated docs reflecting current state

> **Tip:** Each task in the Implementation Schedule should map to one hat and have a demo-able deliverable.

---

## 3) Routing Rules

1. **Start at the Schedule:** Pick a single task from `docs/implementation_schedule.md`. If missing, create a stub task first.
2. **Create a branch:** `feature/<slug>` or `fix/<slug>` and link the task in the session log.
3. **Choose the hat:** Select the role that owns the deliverable; do **only** that scope in this PR.
4. **Validate:** Run local checks; if CI fails, read the failing step logs and reproduce locally.
5. **Close loop:** End session log; open PR referencing the schedule task and checklist items.

**Example Routing:**

- Task: "Add CSV validation for user uploads"
- Hat: **DataOps** (owns validation)
- Branch: `feature/csv-validation`
- Deliverable: Validation function + tests
- Out of scope: UI changes, API endpoint (different hats)

---

## 4) Session Workflow (Required)

- **Open:** Use **Session Start** template → capture objective, plan, and inputs.
- **Execute:** Keep diffs small; narrate major decisions in the log.
- **Close:** Use **Session End** template → summarize work, link artifacts, call out next steps.
- **Commit Discipline:** Clear message: `feat|fix|docs|chore: <scope> [schedule:weekX-taskY]`.

---

## 5) Escalation Triggers (Stop & Ask)

- Schema or API change detected/required
- Secrets/auth/infra configuration touched
- Test changes that alter public behavior or contracts
- Dependency upgrades beyond patch version
- Ambiguous acceptance criteria or conflicting docs
- Failing CI that cannot be reproduced locally in <30 min

> When triggered: document findings in the session log, propose options, and request human review.

---

## 6) Quality Gates (Definition of Done)

A task is **Done** only when:

- Code is merged to `main` and all **Pre-Merge** checks pass.
- Tests cover new logic; coverage not reduced.
- Docs updated where relevant (Charter, KB, README).
- Task status flipped in the Implementation Schedule.

(See detailed checklists in `docs/checklists.md`.)

---

## 7) Planning & Victory Tests

### Planning Mode

For large or risky changes, produce a short plan (bullets, files to edit, tests to add). Do **not** begin edits until plan is acknowledged in the log.

**Planning checklist:**

- [ ] Which files will change?
- [ ] Which tests will be added/modified?
- [ ] Any docs/config updates needed?
- [ ] Estimated size (XS/S/M/L)?
- [ ] Any escalation triggers in scope?

### Victory Test (Prompt → PR)

New agents should run this trivial change to validate toolchain end-to-end:

1. Pick task: "Add version number to CLI help output"
2. Write test: Assert `--version` prints expected format
3. Implement: Add version string to CLI
4. Run: `uv run ruff format . && uv run ruff check . && uv run pytest`
5. Open PR with proper title/labels
6. Verify CI passes

**Success:** PR merged = agent is ready for real work

---

## 8) Minimal Command Palette

```bash
# One-time setup
uv sync && pre-commit install

# Daily loop
uv run ruff format . && uv run ruff check .
uv run pytest -vv

# Docs
mkdocs serve  # http://127.0.0.1:8000
```

---

## 9) PR Rules (Fast Reviews)

- **Scope:** Single task, minimal diff (<300 lines preferred)
- **Title:** `feat|fix|docs|chore: <scope> [schedule:weekX-taskY]`
- **Body:** What/why, links (session log, schedule row), screenshots if UI/CLI
- **Labels:** `size:XS/S/M/L`, `risk:low/med/high`, `area:<module>`
- **Review time:** XS/S = <2hrs, M = <1 day, L requires planning meeting

---

## 10) Common Failure Paths & Fixes

### Code/Test Issues

- **Lint fails:** `uv run ruff check . --fix` then re-run.
- **Tests fail (local):** `uv run pytest -vv -k <pattern>`; capture failing output in log.
- **CI-only failures:** Open failing job; reproduce locally using the same command; attach notes to PR.
- **Import errors:** Verify `pyproject.toml`; run `uv sync`.

### Agent-Specific Issues

- **Context drift:** Summarize progress in session log, clear chat history, resume from log + docs
- **Scope creep:** If you've touched >3 files or >2 hats, stop and split into multiple PRs
- **Stuck >30min:** Document blockers in session log; flag for human review
- **Conflicting instructions:** AI_GUIDE/AGENTS trumps chat history; cite this doc when clarifying

---

## 11) Links (Jump Table)

- **Front Door:** `AI_GUIDE.md`
- **Project Brief:** `docs/project_brief.md`
- **Changelog:** `CHANGELOG.md`
- **Runbook:** `docs/runbook.md`
- **Charter / PRD:** `docs/project_charter.md`
- **Implementation Schedule:** `docs/implementation_schedule.md`
- **Standards & Workflow:** `docs/development_standards.md`
- **Quality Gates & Checklists:** `docs/checklists.md`
- **Session Templates:** `docs/ai_session_templates.md`
- **KB:** `docs/knowledge_base.md`

---

## 12) When to Update This Doc

Update AGENTS.md when:

- Adding/removing agent roles or changing their mandates
- Modifying escalation triggers or quality gates
- Changing core workflow (session templates, routing rules)
- Adding new safety guardrails or "Don't" items
- Updating tooling that affects the command palette

Keep changes atomic and document rationale in git commit message.

---

*Keep this file ≤ ~2 pages. If a section grows, simplify the tool/flow it describes or move details to a dedicated doc under `docs/`.*
