# Security — SpreadSheetz (v0.1)

**Purpose.** Define practical security for MVP now, and a phased roadmap to production. Keep this file short, actionable, and tied to our code + infra choices.

**Scope.** Applies to code (API, ingestion, UI), data (Postgres), developer workflows, and CI/CD. MVP is local‑first; production controls are staged.

---

## 1) Principles

* **Least privilege by default** — only the access needed, only where needed.
* **Defense in depth** — validation at client, API, and DB; audit everything important.
* **Secure by construction** — secrets in env, typed inputs, idempotent writes, provenanced data.
* **Privacy first** — collect the minimum; no PII beyond email for auth.

---

## 2) Data Classification

| Class          | Examples                                               | Storage                                                  | Retention              |
| -------------- | ------------------------------------------------------ | -------------------------------------------------------- | ---------------------- |
| Public         | Setlists, show dates, venues, computed public stats    | Postgres, API cache                                      | Indefinite             |
| Internal       | Ingestion logs, source URLs, correction reviewer notes | Postgres (restricted), logs                              | 18 months              |
| Personal (Low) | User email, attendance toggles                         | Postgres (encrypted at rest in prod), hashed IDs in logs | Until account deletion |

> We do **not** store passwords in MVP; any auth uses provider tokens or local dev secrets.

---

## 3) Secrets Management

* **Local dev**: `.env` (git‑ignored). Example:

  ```dotenv
  DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/spreadsheetz
  SECRET_KEY=change-me
  APP_ENV=dev
  ```
* **CI/CD & staging/prod (Phase 2+)**: use platform secrets store (e.g., GitHub Actions secrets, cloud secret manager). Never echo secrets in logs.
* **Rotation**: every 90 days or on personnel change. Document rotation in `CHANGELOG.md` (no values).

---

## 4) Authentication & Authorization (MVP → Phase 2)

* **MVP (local)**: lightweight session/JWT for attendance marking only. No social sign‑in required.
* **Phase 2**: OAuth/OIDC (GitHub/Google). Store only provider user ID + email.
* **Roles**: `visitor`, `user`, `curator`, `admin`. Admin endpoints behind role checks.
* **Token handling**: short‑lived access tokens; httpOnly cookies preferred for web.

---

## 5) API Security

* **Input validation**: Pydantic schemas; strict types; explicit allowlists for enums.
* **Pagination limits**: default 50, max 200. Reject excessive `per_page`.
* **Rate limits** (Phase 2): 60 req/min per IP (public), 120 req/min (authenticated). Bursting allowed with token bucket.
* **Error responses**: no stack traces in production; structured errors only.
* **CORS**: allow only our UI origin in staging/prod.
* **Compression**: disable compression for auth endpoints (BREACH‑like concerns) if sensitive.

---

## 6) Database Security

* **Principle**: API uses a restricted DB role with only needed privileges.
* **Constraints**: enforce NOT NULL, CHECKs, UNIQUE natural keys, and FKs.
* **Audit**: `correction_log` writes include `who`, `when`, `reason`, and `source`.
* **Migrations**: never drop a column with data without an archival step.
* **Backups (Phase 2)**: daily full + 7‑day PITR window.

---

## 7) Ingestion & Scraping Ethics

* **Robots & Terms**: respect robots.txt where applicable; comply with source ToS.
* **Politeness**: rate limit requests; randomize user agent within a small set; exponential backoff.
* **Provenance**: capture `source`, `source_ref`, `ingested_at`; avoid republishing long‑form scraped content verbatim.
* **Quarantine**: isolate raw fetch/parse errors; do not partially commit malformed records.

---

## 8) Logging, Monitoring, and PII

* **Structured logs**: JSON lines with `ts`, `level`, `component`, `request_id`.
* **No secrets/PII** in logs; hash emails to an internal ID where correlation is needed.
* **Metrics**:  ingest success rate, dedupe ratio, API p95 latency, error rates.
* **Trace IDs**: propagate request IDs across API ↔ DB (via logs) for audits.

---

## 9) Frontend Security (Minimal UI)

* **CSP** (Phase 2): default‑src 'self'; script‑src 'self'; connect‑src our API; img‑src 'self' data:; style‑src 'self' 'unsafe-inline' (until CSS hardening).
* **XSS**: never `dangerouslySetInnerHTML`; encode user content; strip HTML from notes.
* **Storage**: prefer cookies (httpOnly) over localStorage for tokens.

---

## 10) Compliance Posture (Roadmap)

* **MVP**: internal project, no regulated data.
* **Phase 2**: document data flows, third‑party sources, and licenses.
* **Phase 3**: basic SOC2‑style hygiene: access reviews, change management, backup/DR tests.

---

## 11) Vulnerability Management

* **Dependencies**: weekly SCA (`pip-audit` or `uv pip audit`; `npm audit --production`).
* **Pinning**: use lock/pinned versions; renovate/bot or manual updates.
* **Patching**: critical vulns patched within 72h; note in `CHANGELOG.md`.

Commands:

```bash
uv pip install pip-audit && uv run pip-audit
npm audit --omit=dev
```

---

## 12) Incident Response (Lightweight)

1. **Detect**: error spikes, anomalous traffic, or data integrity alarms.
2. **Stabilize**: rate‑limit or temporarily disable affected endpoints.
3. **Triage**: identify blast radius; gather logs (by request ID/time window).
4. **Fix**: patch code/config; write a regression test.
5. **Report**: add an entry to `docs/decisions/incident_<YYYYMMDD>_<slug>.md`.
6. **Prevent**: create a follow‑up RFC/issue; add a guardrail (lint/test/constraint).

---

## 13) Access Control & Environments

* **Local dev**: single developer role; `.env`‑based config; Docker Postgres exposed only to localhost.
* **Staging/Prod (Phase 2)**: separate service accounts per environment; network allowlists; no shared admin passwords.
* **Admin UI/API**: behind auth; capture reviewer identity in `correction_log`.

---

## 14) Data Retention & Deletion

* **User data**: delete attendance and email upon account deletion request.
* **Logs**: retain 90 days in staging/prod, 14 days in dev if centralized.
* **Backups**: follow DB policy; ensure deletion propagates after retention window.

---

## 15) Checklists

### Pre‑PR Security Checks

* [ ] Inputs validated (Pydantic) and typed
* [ ] No secrets/PII in logs or error messages
* [ ] Pagination caps enforced; endpoints rate‑limit aware
* [ ] DB migrations safe (no data loss without archive)
* [ ] Tests include negative cases and boundary values

### Pre‑Release (Phase 2+)

* [ ] Secrets in managed store; rotated ≤ 90 days
* [ ] CORS restricted to known origins
* [ ] Rate limiting enabled at edge/API
* [ ] Backups configured and tested
* [ ] CSP headers set for UI

---

## 16) Threat Model (STRIDE snapshot)

| Threat                 | Area            | Mitigation                                                           |
| ---------------------- | --------------- | -------------------------------------------------------------------- |
| Spoofing               | Auth tokens     | Short‑lived tokens; httpOnly cookies; verify signatures              |
| Tampering              | Corrections     | `correction_log` with reviewer identity; limited admin role          |
| Repudiation            | Admin actions   | Structured audit logs; immutable history                             |
| Information Disclosure | API responses   | Field allowlisting; avoid sensitive fields; pagination & rate limits |
| Denial of Service      | API & ingest    | Rate limiting; timeouts; concurrency caps                            |
| Elevation of Privilege | Admin endpoints | Role checks; no default admin; separate service accounts             |

---

## 17) References

* `docs/runbook.md` — ops & troubleshooting
* `docs/database_schema.md` — constraints and audit tables
* `docs/development_standards.md` — coding & review requirements
* `docs/system_overview.md` — architecture & data flow

---

**Ship small, audit always, and never store what you don’t need.**
