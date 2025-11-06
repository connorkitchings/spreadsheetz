# Knowledge Base — External Sources (Focused on Everyday Companion & TourWrangler)

> **Purpose.** This page is the single source of truth for how we **discover, ingest, attribute, and maintain** external Widespread Panic setlist data from **Everyday Companion (EC)** and **TourWrangler (TW)**. This intentionally excludes Panicstream per project direction.

**Scope:** Widespread Panic (WSP) official shows; side projects are out-of-scope unless explicitly marked.

---

## 1) Source Overview

| ID | Source             | Coverage                        | Data Types                                                       | Access Pattern                    | Notes                                                                                                                              |
| -- | ------------------ | ------------------------------- | ---------------------------------------------------------------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| ec | Everyday Companion | 1986 → present (varies by tour) | Show dates, venues, cities, setlists, guests, notes, rarities    | Public web pages                  | Canonical community reference for WSP setlists; human‑curated with notes. Treat as primary reference when conflicts arise with TW. |
| tw | TourWrangler       | 2000s → present (varies)        | Show dates, venues, setlists, user annotations, attendance tools | Public web pages + per‑show pages | Often faster to update during active tours; treat as secondary corroboration when EC is silent or delayed.                         |

**Primary vs Secondary:** EC = primary; TW = secondary corroboration. Conflicts resolved by curator review (see §7 Corrections & Conflicts).

---

## 2) Ingestion Ethics & Legal Considerations

We follow a **"respect first"** ingestion model.

* **Robots/ToS:** Check robots.txt and terms of service before any scrape. If disallowed, do not scrape; prefer **manual import** or **user-provided exports**.
* **Rate limits:** Default to ≤ 0.5 requests/sec per host, burst ≤ 1, with backoff (2x, max 60s). Night runs only (local time 01:00–05:00) unless on-demand.
* **Attribution:** Every record carries `source_id` (`ec` or `tw`) and `source_url`. The UI must visibly attribute the source on show pages (see §9 Attribution in UI).
* **Respect value:** Do not replicate entire sites; ingest only **facts** (dates, songs played) and minimal context necessary to power features.
* **Contact channel:** Maintain an email (e.g., `data@spreadsheetz.app`) for takedowns or correction requests from maintainers.

---

## 3) Field Mapping & Normalization

This section defines how we map EC/TW page elements into our canonical schema. Our core tables (see `database_schema.md`) include: `artist`, `venue`, `show`, `set`, `set_song`, `song`, `guest`, `annotation`.

### 3.1 Show-Level

| Canonical Field  | From EC                     | From TW                 | Notes                                                   |
| ---------------- | --------------------------- | ----------------------- | ------------------------------------------------------- |
| artist_slug      | implicit (Widespread Panic) | implicit                | Fixed to `wsp` for this KB.                             |
| show_date (date) | page title/header           | listing row / show page | Normalize to ISO `YYYY-MM-DD`.                          |
| venue_name       | header block                | header block            | Apply venue alias resolution (see §4.2).                |
| city             | header block                | header block            | Split `City, ST` → `city`, `region_code`.               |
| country_code     | inferred                    | inferred                | Default `US` unless otherwise stated.                   |
| source_id        | `ec`                        | `tw`                    | Required.                                               |
| source_url       | page URL                    | page URL                | Required for provenance.                                |
| notes_raw        | page notes                  | page notes              | Store raw; parsed annotations go to `annotation` table. |

### 3.2 Set & Song-Level

| Canonical Field | From EC                        | From TW        | Notes                                            |
| --------------- | ------------------------------ | -------------- | ------------------------------------------------ |
| set_order       | section order                  | section order  | `1,2,3,encore,encore2` mapped to numeric + flag. |
| song_position   | list index                     | list index     | 1-based per set.                                 |
| song_name_raw   | list item text                 | list item text | Normalize via `song` alias map (see §4.1).       |
| segue           | separators like `→`, `>`, `->` | same           | Map to boolean `segue_next` + `segue_symbol`.    |
| guest_raw       | inline `(with X)`              | inline         | Parsed to `guest` table (Phase 2 if not MVP).    |
| tease_raw       | inline `[Tease: Y]`            | inline         | Parsed to `annotation` with `type='tease'`.      |

---

## 4) Data Quality Rules

### 4.1 Song Alias Resolution

A curated CSV/JSON alias map powers normalization (e.g., `Barstools and Dreamers` ≡ `Barstools`, `Airplane` ≡ `The Airplane`). Rules:

* **Exact match** → canonical `song_id`.
* **Case/diacritics** insensitive.
* **Common abbreviations** (e.g., `Diner >`) handled before segue parsing.
* **Unresolved** names land in `song_pending` for curator review.

### 4.2 Venue Alias Resolution

* Maintain `venue_alias(venue_alias, venue_id)` with start/end dates for renamed venues.
* Prefer canonical `venue_id` by **(name, city, region, country)** with fuzzy match threshold 92/100.

### 4.3 Duplicate Show Detection

* Potential dupes if **(date, city, venue_name)** match across sources.
* Keep one `show` record; attach multiple `source_*` rows in `show_source` bridge.

### 4.4 Ordering & Encore Logic

* `encore` sections come **after** final main set; multi‑encores use `encore_order = 1..N`.
* If a site embeds encore songs inside Set II footer text, split into distinct `encore` sets.

---

## 5) Crawler/Parser Contracts

### 5.1 Everyday Companion (ec)

* **Discovery:** Tour index → year pages → show pages.
* **Per‑show selectors:**

  * Title block → date, venue, city/state
  * Setlist lists (ordered) → sets/songs
  * Inline notes → `notes_raw`
* **Edge cases:**

  * Old shows may have partial or uncertain songs marked with `?`; store as `confidence = 'low'` and keep text.
  * Some jam/tease notes appear as brackets; capture as `annotation` rows.

### 5.2 TourWrangler (tw)

* **Discovery:** Year index → show list → show page.
* **Per‑show selectors:** Similar to EC; page structure can differ by year.
* **Edge cases:**

  * Draft/placeholder pages during tours; treat as `status='provisional'` and re‑crawl within 72h.
  * User comments sometimes include additional songs; treat comments as **unverified** until corroborated.

**Retry/Backfill Policy:** If either source shows provisional or partial data, schedule a **weekly backfill** for 6 weeks post‑show.

---

## 6) Rate, Pagination, and Backoff

* **Baseline:** 1 request / 2 seconds, concurrency = 1.
* **Backoff:** Exponential (2x) on 4xx/5xx, jitter 10–25%.
* **Pagination:** Use site navigation rather than query params; parsers must be resilient to next/prev year jumps.
* **Timeouts:** 20s connect/read; total job budget ≤ 15 minutes per source.

---

## 7) Corrections & Conflicts

**Hierarchy:** EC > TW > User report.

**Playbook:**

1. Log discrepancy with `show_id`, fields in conflict, both `source_url`s.
2. Attempt corroboration (another reputable source, taper notes, official WSP post).
3. If unresolved: prefer EC; add `annotation(type='disputed', body=...)` and set `data_confidence='medium'`.
4. Record action in `audit_log` with actor, timestamp, rationale.

**User-Facing:** Display a small **“Disputed data”** banner with both claims and sources.

---

## 8) Data Freshness & Recrawl Cadence

* **Active tour:** TW daily, EC every 3 days.
* **Off-tour:** Weekly check on both sources for retro edits.
* **Historical backfills:** Quarterly sweep on pre‑2000 shows.

---

## 9) Attribution in UI

* On every show page, render: `Setlist © Everyday Companion` or `Data courtesy of TourWrangler`, linked to the source URL.
* On aggregated pages (stats, search): show a compact pill listing contributing sources for that row.
* In CSV export: include `source_id` and `source_url` columns.

---

## 10) Operational Checklists

### 10.1 Pre‑Deploy Parser Checks

* [ ] Unit parse 3 shows per decade per source.
* [ ] Verify alias maps (songs, venues) load and produce stable IDs.
* [ ] Verify encore detection on 3 known edge‑case shows.

### 10.2 Nightly Job SLOs

* [ ] < 1% parser failures across all fetched pages.
* [ ] < 0.1% newly created `song_pending` rows (guard against alias drift).
* [ ] All new/changed shows have `source_url` populated.

### 10.3 Manual Curation

* [ ] Clear `song_pending` weekly.
* [ ] Review `disputed` annotations within 7 days.

---

## 11) Change Log (this file)

* **2025‑11‑06:** Refocused KB on **Everyday Companion** and **TourWrangler** only. Added ingestion ethics, field mapping tables, rate limits, conflict resolution, and attribution guidance.

---

## 12) New Band Onboarding Checklist

* [ ] Add sources to KB table; verify ToS/robots
* [ ] Create slug; seed `artist` row
* [ ] Implement adapter; canonicalize fields; idempotent upsert
* [ ] Add fixtures/tests; run `pytest`
* [ ] Add to `BAND_LIST_JSON` and CLI routing
* [ ] Update `CHANGELOG.md`
