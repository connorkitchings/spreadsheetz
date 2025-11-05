# Implementation Schedule — {{PROJECT_NAME}}

This implementation schedule outlines a structured, week-by-week plan to deliver **{{PROJECT_NAME}}**, a {{TYPE}} project, over approximately **{{DURATION_WEEKS}}**. It assumes a repo-first workflow with AI-assisted development, a small team shaped as **{{TEAM_SIZE_AND_ROLES}}**, and dependencies such as **{{DEPENDENCIES}}** being available on time. Treat this as a living document: update tasks, owners, and dates as the project evolves, and use session logs to capture decisions and deviations from plan.

**Status Legend:** ☐ Not Started · ▶ In Progress · ✅ Done · ⚠ Risk/Blocked

---

## Week-by-Week Schedule

> Adjust weeks, tracks, and owners as needed. Keep each task demo-able by the end of its week.

### Week 1 — Foundation & Direction

| Week   | Track     | Task                                                            | Owner                  | Deliverable                                                   | DoD/Checklist         | Status       | Notes/Dependencies                      |
|--------|-----------|-----------------------------------------------------------------|------------------------|---------------------------------------------------------------|-----------------------|-------------|------------------------------------------|
| Week 1 | DevEx/CI  | Initialize repo structure and configure basic branching model    | Connor Kitchings       | Repo with base folders and initial CI config committed       | [DoD: Setup]          | ✅ Done       | Base scaffold in place; branch strategy captured in docs     |
| Week 1 | Docs      | Create front-door docs (README, [Project Brief](./project_brief.md))             | Connor Kitchings       | `README.md` + `docs/project_brief.md` updated for template    | [DoD: Docs]           | ✅ Done       | Project brief completed 2025-11-05                           |
| Week 1 | Discovery | Clarify problem statement, scope, and non-goals                 | Connor Kitchings       | Updated project brief & charter capturing scope/non-goals    | [DoD: Scope]          | ✅ Done       | See `docs/project_brief.md` & `docs/project_charter.md`       |
| Week 1 | DevEx/CI  | Set up dev environment and CI stub (lint/test placeholder)      | DevEx Guild            | CI job that runs basic checks on push                        | [DoD: Testing]        | ▶ In Progress | `.github/workflows/ci.yml` ready; validate on next pipeline   |
| Week 1 | DataOps   | Validate access to core dependencies (APIs, datasets, secrets)   | DataOps Working Group  | “Access check” notebook/log with pass/fail status            | [DoD: Dependencies]   | ☐ Not Started | Pending dependency inventory from stakeholders               |
| Week 1 | Docs      | Close loop with session log (capture key setup decisions)       | Connor Kitchings       | Week 1 session log entry linked from project brief           | [DoD: Session Log]    | ✅ Done       | Logged in `session_logs/2025-11-05.md`                        |

---

### Week 2 — DataOps & Pipeline Skeleton

| Week   | Track     | Task                                                            | Owner                  | Deliverable                                                   | DoD/Checklist         | Status       | Notes/Dependencies                      |
|--------|-----------|-----------------------------------------------------------------|------------------------|---------------------------------------------------------------|-----------------------|-------------|------------------------------------------|
| Week 2 | DataOps   | Implement ingestion script v1 for core data/API                 | DataOps                | Ingestion script + config for main source                     | [DoD: Data Quality]   | ☐ Not Started | Requires stable source schema            |
| Week 2 | DataOps   | Define data schema and storage layout (raw/processed zones)     | DataOps                | Schema doc + directory/table layout                           | [DoD: Schema]         | ☐ Not Started | Align with existing data conventions     |
| Week 2 | DataOps   | Add basic validation checks (schema, ranges, nulls)             | DataOps                | Validation module and sample run report                       | [DoD: Data Quality]   | ☐ Not Started | Integrate with ingestion script          |
| Week 2 | DevEx/CI  | Wire ingestion into CI-friendly job or manual run script        | DevEx/CI               | Script or CI job that runs ingestion on demand                | [DoD: Automation]     | ☐ Not Started | Coordinate schedule with infra teams     |
| Week 2 | DevEx/CI  | Capture logs/metrics for ingestion (basic observability)        | DevEx/CI               | Log/metric fields defined and stored                          | [DoD: Monitoring]     | ☐ Not Started | Minimal overhead to start                |
| Week 2 | Docs      | Close loop with session log (DataOps decisions, schema tradeoffs) | Docs / PM            | Week 2 session log entry with link to schema & ingestion docs | [DoD: Session Log]    | ☐ Not Started | Reference validation and issues          |

---

### Week 3 — Features & Core Logic / Modeling

| Week   | Track        | Task                                                         | Owner                  | Deliverable                                                   | DoD/Checklist         | Status       | Notes/Dependencies                      |
|--------|--------------|--------------------------------------------------------------|------------------------|---------------------------------------------------------------|-----------------------|-------------|------------------------------------------|
| Week 3 | Feature Eng  | Build feature table or core transformed dataset v1           | DataOps / Feature Eng  | Reproducible feature table / transformed dataset             | [DoD: Data Quality]   | ☐ Not Started | Inputs: Week 2 ingestion + schema        |
| Week 3 | Modeling     | Implement baseline model or core business logic v1           | Modeler / Backend      | Baseline implementation with saved outputs                   | [DoD: Modeling]       | ☐ Not Started | Define simple baseline metric            |
| Week 3 | Modeling     | Run evaluation / QA and capture metrics                      | Modeler / Analyst      | Metrics report (accuracy, latency, or domain metrics)        | [DoD: Evaluation]     | ☐ Not Started | Compare vs naive baseline                |
| Week 3 | Docs         | Draft model/logic card stub (assumptions, inputs, outputs)   | Docs / PM              | Model/logic card in `docs/models/` or `docs/architecture/`   | [DoD: Docs]           | ☐ Not Started | Include key tradeoffs                    |
| Week 3 | Docs         | Close loop with session log (baseline results & decisions)   | Docs / PM              | Week 3 session log entry with links to metrics & card        | [DoD: Session Log]    | ☐ Not Started | Note open questions for Week 4           |

---

### Week 4 — Productization & Interface

| Week   | Track     | Task                                                            | Owner                  | Deliverable                                                   | DoD/Checklist         | Status       | Notes/Dependencies                      |
|--------|-----------|-----------------------------------------------------------------|------------------------|---------------------------------------------------------------|-----------------------|-------------|------------------------------------------|
| Week 4 | App/UI    | Create CLI or UI stub to expose core functionality              | Frontend / App         | Minimal CLI commands or UI screen wired to sample data        | [DoD: UX]             | ☐ Not Started | Focus on clarity over polish             |
| Week 4 | App/UI    | Wire live pipeline/logic into CLI/UI (happy-path only)          | Frontend / Backend     | End-to-end flow from input to output in dev environment      | [DoD: Integration]    | ☐ Not Started | Uses Week 3 baseline logic               |
| Week 4 | DevEx/CI  | Externalize configuration (env files, config layer)             | DevEx/CI               | Config pattern documented and used by ingestion & logic      | [DoD: Config]         | ☐ Not Started | Avoid secrets in code                    |
| Week 4 | DevEx/CI  | Implement basic artifact/versioning approach                    | DevEx/CI               | Strategy for tagging releases/artifacts documented            | [DoD: Release Ready]  | ☐ Not Started | Reuse org standards if available         |
| Week 4 | Docs      | Close loop with session log (UI/product decisions, UX notes)    | Docs / PM              | Week 4 session log entry with links to UI/CLI screenshots    | [DoD: Session Log]    | ☐ Not Started | Capture feedback from early testers      |

---

### Week 5 — Hardening, Tests, and Operability

| Week   | Track     | Task                                                            | Owner                  | Deliverable                                                   | DoD/Checklist         | Status       | Notes/Dependencies                      |
|--------|-----------|-----------------------------------------------------------------|------------------------|---------------------------------------------------------------|-----------------------|-------------|------------------------------------------|
| Week 5 | DevEx/CI  | Expand automated test coverage (unit + key integration paths)   | DevEx/CI               | Test suite covering critical paths with pass/fail indicators | [DoD: Testing]        | ☐ Not Started | Prioritize high-risk code paths          |
| Week 5 | DevEx/CI  | Add monitoring / alert hooks for critical failures              | DevEx/CI               | Monitoring/alerts defined for key jobs or endpoints          | [DoD: Monitoring]     | ☐ Not Started | Integrate with existing tooling          |
| Week 5 | Modeling  | Run performance/latency pass and optimize bottlenecks           | Modeler / Backend      | Summary of perf issues + implemented fixes                   | [DoD: Performance]    | ☐ Not Started | Include before/after metrics             |
| Week 5 | Docs      | Complete security/privacy checklist first pass                  | Docs / PM              | Checklist doc with status of each control                    | [DoD: Security]       | ☐ Not Started | Coordinate with org security guidelines  |
| Week 5 | Docs      | Define failure playbook / [Runbook](./runbook.md)                              | Docs / PM              | Runbook with common failure modes and recovery steps         | [DoD: Ops]            | ☐ Not Started | Link to monitoring/alert setup           |
| Week 5 | Docs      | Close loop with session log (hardening decisions, tradeoffs)    | Docs / PM              | Week 5 session log entry with links to tests & runbook       | [DoD: Session Log]    | ☐ Not Started | Note deferred hardening items            |

---

### Week 6 — Release, Demo, and Next Phase

| Week   | Track     | Task                                                            | Owner                  | Deliverable                                                   | DoD/Checklist         | Status       | Notes/Dependencies                      |
|--------|-----------|-----------------------------------------------------------------|------------------------|---------------------------------------------------------------|-----------------------|-------------|------------------------------------------|
| Week 6 | Docs      | Polish user-facing docs (quickstart, FAQs, troubleshooting)     | Docs / PM              | Updated docs section ready for external readers              | [DoD: Docs]           | ☐ Not Started | Ensure examples are copy-paste friendly  |
| Week 6 | App/UI    | Prepare and run internal/external demo                          | Frontend / Project Lead| Demo script + recorded walkthrough or slides                 | [DoD: Demo]           | ☐ Not Started | Invite key stakeholders                  |
| Week 6 | DevEx/CI  | Cut v1 tagged release and [Changelog](../CHANGELOG.md)                             | DevEx/CI               | Tagged release, changelog entry, and release notes           | [DoD: Release Ready]  | ☐ Not Started | Coordinate with release processes        |
| Week 6 | Docs      | Capture retro and define next-phase backlog                     | Docs / PM              | Retro notes + prioritized backlog in tracker                 | [DoD: Retro]          | ☐ Not Started | Include “stop/start/continue” insights   |
| Week 6 | Docs      | Close loop with session log (release, retro, next-phase plan)   | Docs / PM              | Week 6 session log entry with key decisions                  | [DoD: Session Log]    | ☐ Not Started | Link to retro and backlog                |

> For projects longer than 6 weeks, clone one or more weeks and adapt tasks to your extended scope (e.g., advanced modeling, UX polish, new integrations).

---

## Milestones

> Replace or refine targets using **{{MILESTONES}}** if provided.

- **Foundation Ready (Target: End of Week 1)**  
  - **Success:** Repo initialized, docs front-door in place, and CI stub running.  
  - **Demo:** Walkthrough of repo structure, README, and a passing CI run.

- **Data Pipeline v1 (Target: End of Week 2)**  
  - **Success:** Ingestion script runs on demand, data stored using agreed schema, basic validation in place.  
  - **Demo:** Run ingestion in front of stakeholders and show validation outputs.

- **Baseline Logic/Model Ready (Target: End of Week 3)**  
  - **Success:** Baseline algorithm or model runs end-to-end with metrics captured and documented.  
  - **Demo:** Present metrics report and model/logic card; compare to naive baseline.

- **Productized Interface Demo (Target: End of Week 4)**  
  - **Success:** CLI or UI stub triggers real logic on live or realistic data.  
  - **Demo:** Live walk-through of main user flow in dev environment.

- **Hardening Pass Complete (Target: End of Week 5)**  
  - **Success:** Core tests, monitoring, and runbook in place; high-risk issues addressed.  
  - **Demo:** Show test coverage summary, monitoring hooks, and runbook.

- **v1 Release (Target: End of Week 6)**  
  - **Success:** v1 tagged, docs polished, and retro plus next-phase backlog agreed.  
  - **Demo:** v1 release notes + final demo of “happy path” scenario.

---

## Risks & Mitigations

| Risk                                                       | Impact                              | Mitigation / Plan                                                       | Owner          | Trigger to Escalate                                |
|------------------------------------------------------------|-------------------------------------|--------------------------------------------------------------------------|----------------|----------------------------------------------------|
| External dependencies ({{DEPENDENCIES}}) delayed or revoked| Slips in ingestion, modeling, or UI | Identify fallback sources; design stubs; timebox waiting before re-plan | Project Lead   | Dependency not available by mid-Week 2            |
| Data quality issues (missing, inconsistent, drift)         | Poor model/logic performance        | Add validation, profiling, and data contracts early                     | DataOps        | >5% rows failing validation for a full week       |
| Scope creep from stakeholders                              | Timeline and quality risk           | Maintain explicit non-goals; use change log and milestone gates         | PM / Lead      | More than 2 major scope changes in 2 weeks        |
| CI or infra instability                                   | Reduced developer velocity          | Keep scripts runnable locally; isolate flaky checks; add retries        | DevEx/CI       | CI red >30% of runs for 3 consecutive days        |
| Lack of user/UX feedback                                   | Misaligned product experience       | Schedule early demos; use simple feedback form after each milestone     | Frontend / PM  | No UX feedback by end of Week 4                   |
| Key person risk (solo or thin coverage on core component)  | Blocked progress if unavailable     | Document critical paths; cross-train where possible                     | Project Lead   | Core owner unavailable for >3 working days        |

---

## Change Log

| Date       | Change                          | Reason                                  | Owner        |
|------------|---------------------------------|-----------------------------------------|-------------|
| 2025-01-01 | Initial implementation schedule | Create baseline plan for the project    | Project Lead |

> Add a new row whenever you significantly shift scope, dates, or milestones.

---

## Roll-up Kanban

> Keep these lists short and maintain them weekly.

### Backlog

- Expand feature engineering / transformation logic.
- Advanced evaluation or experiment suite.
- Additional UI/UX polish and accessibility improvements.
- Integration with downstream systems or consumers.
- Extended monitoring dashboards and alerts.

### In Progress

- Initialize repo structure and CI stub (Week 1).  
- Define problem statement, scope, and non-goals.  
- Validate access to core dependencies (APIs, datasets, secrets).

### Done

- Implementation schedule drafted and committed to `docs/implementation_schedule.md`.

---

## How to Use This Schedule

This schedule is a **living artifact**. Treat it as the single place where the project’s week-by-week plan, milestones, and risks are tracked. Update it in the repo as work progresses and reference it in session logs and standups.

- Update **Status** as work progresses:  
  - `☐ Not Started` → `▶ In Progress` → `✅ Done`.  
  - Use `⚠ Risk/Blocked` when a dependency or issue stops progress.
- Turn each **DoD anchor** (e.g., `[DoD: Testing]`, `[DoD: Data Quality]`) into a link once you create detailed checklists, for example:  
  - `[DoD: Testing](../checks/dod_testing.md)`
- After any meaningful change (scope, dates, new milestone), add a row in the **Change Log** and summarize it in the next session log.
- At least once per week (and at each major milestone), run a short ritual:  
  - Review each week’s tasks and statuses.  
  - Adjust upcoming weeks based on new information.  
  - **Close the loop with a session log** capturing decisions, risks, and next steps, and link back to this schedule.

By keeping this document current, you give both humans and AI agents a clear, shared picture of where the project stands and what needs to happen next.
