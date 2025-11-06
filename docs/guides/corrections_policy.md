# Corrections Policy — Intake → Verify → Apply → Audit → Notify

> **Purpose.** Define a consistent, respectful, and auditable process for handling data corrections and disputes sourced from the community and external references. This policy focuses on **Everyday Companion (EC)** as primary and **TourWrangler (TW)** as secondary, per our Knowledge Base. Panicstream is out-of-scope.

**Applies to:** WSP shows, sets, songs, guests, teases, jam flags, venues.
**Audiences:** Curators, Developers, Support.

---

## 1) Principles

* **Respect**: Honor the effort of EC and TW maintainers; attribute clearly; ingest only necessary factual data.
* **Provenance**: Every change must be tied to a `source_id` and `source_url` (or `curator` with rationale).
* **Transparency**: Publicly visible change notes for disputed items.
* **Reversibility**: All edits are idempotent and revertible (audit log, point-in-time recovery).

---

## 2) What Qualifies as a Correction?

* Setlist facts: added/removed songs, order adjustments, encore labeling, segue symbols.
* Show metadata: date, venue, city/region/country, cancellation/postponement markers.
* Guests/teases/jam flags: presence, identity, length, confidence.
* Song/venue canonicalization: alias mapping updates.

---

## 3) Intake Channels

* **Email**: `data@spreadsheetz.app` (preferred; auto-acknowledged).
* **In‑app form**: "Suggest a correction" button on show pages.
* **GitHub issue**: `type: data-correction` template (for power users).

**Required fields** (all channels):

* Show link (our app URL) + source link(s) (EC/TW).
* Correction type (drop‑down) and details.
* Your name (optional) + contact email (optional).

---

## 4) Triage & SLA

* **P1 (blocking/incorrect core fact)**: wrong date/venue, wrong setlist order → **48h**.
* **P2 (completeness/flags)**: missing encore, tease, jam length → **5 business days**.
* **P3 (cosmetic/alias)**: alias/typo, capitalization → **2 weeks** batch.

Queue is FIFO within priority; P1 can preempt.

---

## 5) Verification Rules (EC Primary)

**Decision matrix:**

| Scenario             | EC | TW | Action                                                                                        |
| -------------------- | -- | -- | --------------------------------------------------------------------------------------------- |
| EC and TW agree      | ✓  | ✓  | Apply change; set `data_confidence='high'`.                                                   |
| EC disagrees with TW | ✗  | ✓  | Prefer **EC**; apply EC; add `annotation(type='disputed')` with both claims.                  |
| EC silent, TW claims | —  | ✓  | Apply TW with `data_confidence='medium'`; schedule recrawl in 3 days.                         |
| Neither EC nor TW    | —  | —  | Hold. Request corroboration (taper notes, official posts). Add GitHub label `needs-evidence`. |

**Minimum evidence** to flip an existing fact: EC or 2 independent reputable sources. For teases/jam lengths, allow TW + 1 corroboration (e.g., taper timing) at `medium` confidence until EC posts.

---

## 6) Edit Workflow (Curator)

1. **Open Case**: Create a correction record referencing `show_id`, fields in question, links.
2. **Review Evidence**: Capture screenshots/notes if needed.
3. **Stage Change**: Apply to a draft environment (feature flag or `dry_run=true` job) and run validations:

   * Set order uniqueness; encore placement; no gaps in `song_position`.
   * Aliases resolve to canonical `song_id`; new aliases open a curator task.
4. **Apply**: Merge to prod via standard deploy or curator tool; ensure `show_source` rows remain intact.
5. **Annotate**: If sources conflict, add `annotation(type='disputed', body=...)` with both claims and dates.
6. **Audit**: Write to `audit_log` (see §7) with actor + rationale.
7. **Notify**: Send acknowledgments/closure emails (templates in §10).

---

## 7) Audit & Provenance

### 7.1 audit_log (system table)

* `id` ULID, `entity` (show/set/set_song/venue/song), `entity_id`, `action` (create/update/delete), `diff` jsonb, `actor` (curator/bot/email), `source_id`, `source_url`, `rationale` text, `created_at` timestamptz.

### 7.2 show_source

* Maintain at least one row per show; update `first_seen_at` only when first added. Do **not** rewrite provenance on later edits; add `annotation` instead if the source changed the claim later.

---

## 8) Disputes & Reversions

* **Open dispute**: Keep current fact aligned to EC; mark `annotation='disputed'`; set `data_confidence='medium'` if the dispute is material.
* **Resolution**: When EC updates, flip data, close dispute, add close‑note to `audit_log` with links.
* **Revert**: Any edit is revertible via audit diff. Emergency revert allowed by on‑call curator.

---

## 9) Privacy & Legal

* Do not store personal data from reporters beyond optional name/email.
* Respect robots/ToS; no bulk replication beyond factual excerpts needed for features.
* Take‑down: If a maintainer requests removal of specific derived content, escalate to project owner within 24h.

---

## 10) Communication Templates

### 10.1 Auto‑ack (intake)

> Subject: We received your correction for [Show: {date} — {city}]
> Thanks! Ticket #{id} is open. We’ll review within {SLA}. We’ll update you when it’s resolved.

### 10.2 Needs evidence

> Subject: More info needed for [Show: {date} — {city}]
> We couldn’t verify this change yet. If you have links (EC, TW, taper notes, official posts), please reply and we’ll proceed.

### 10.3 Resolved

> Subject: Correction applied for [Show: {date} — {city}]
> We’ve updated the listing. Provenance: {source_label}. Changelog: {audit_link}. Thank you for improving the dataset!

---

## 11) UI/UX Requirements

* **Show page**: Display a small "Data source" pill (EC/TW) with link; show a "Suggest a correction" button.
* **Disputed state**: Banner with brief text + both claims; link to details.
* **History**: Collapsible “Change history” fed from `audit_log` (last 5 entries).

---

## 12) API Touchpoints

* `POST /corrections` (public, rate‑limited): creates intake ticket (not a direct DB edit).
* `GET /shows/{id}`: include `data_confidence`, `disputed` boolean, and `sources[]`.
* `GET /shows/{id}/history`: audit entries.
* `POST /curation/apply` (curators): applies staged changes.

---

## 13) Metrics & SLOs

* Mean time to close by priority (P1 ≤ 48h, P2 ≤ 5d, P3 ≤ 14d).
* % disputes resolved by EC updates.
* Parser recrawl success after corrections (3‑day window).
* Reporter satisfaction (thumbs up/down on closure email).

---

## 14) Checklists

### Curator Checklist

* [ ] Confirm EC/TW links provided.
* [ ] Classify P1/P2/P3 and set SLA.
* [ ] Verify aliases and canonical IDs.
* [ ] Stage + validate + apply.
* [ ] Add annotation if disputed; set confidence.
* [ ] Audit log updated.
* [ ] Notify reporter.

### Developer Checklist

* [ ] Endpoint `POST /corrections` validation & rate limit.
* [ ] Audit middleware writes `diff` and `actor`.
* [ ] Feature flags for staged apply.
* [ ] Backfill job schedules recrawl when `data_confidence!='high'`.

### General Corrections Workflow

* [ ] Confirm discrepancy with two sources (or primary update)
* [ ] Prepare delta (before → after) with reason
* [ ] Apply via admin API/SQL (idempotent)
* [ ] Append to `correction_log` (who, when, reason, source)
* [ ] If non‑trivial, add a note in `docs/decisions/`

---

## 15) Change Log (this file)

* **2025‑11‑06:** Initial version aligned to EC primary / TW secondary policy; end‑to‑end workflow, SLAs, decision matrix, templates, and checklists.
