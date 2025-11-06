# Glossary — SpreadSheetz (v0.1)

Short, unambiguous definitions used across code, docs, and UI. If a term changes,
update here first.

---

## A

**Alias (song alias)** — An alternate spelling or title that maps to a canonical song
title.

**Attendance** — A user’s recorded presence at a specific show (`attendance` table;
key `(user_id, show_id)`).

**Artist** — A canonical band identity (e.g., `wsp`, `goose`).

---

## B

**Band slug** — Lowercase short code for an artist used in URLs, CLIs, and configs.

**Backfill** — Historical ingestion to fill gaps prior to the MVP focus window.

---

## C

**Canonicalization** — The process of normalizing names (songs, venues) to a single
accepted form.

**Correction** — A curator‑approved change to stored data, recorded in `correction_log`
with provenance and reviewer identity.

**Core stats** — Frequency, gaps, streaks, openers/closers, and related aggregates
served by the stats service.

**Cursor (pagination)** — A token that encodes the next page position for API list
endpoints.

---

## D

**Deduplication (dedupe)** — Detecting and preventing duplicate rows, usually via natural keys.

**Definition of Done (DoD)** — The checklist that must be true for a PR to merge.

---

## E

**Encore** — A set after the main sets, with its own ordered `position` within a show.

---

## F

**Foreign key (FK)** — A database constraint linking a column to a primary key in
another table.

---

## G

**Gap** — Number of shows since a song’s last performance for a given artist,
computed from ordered `set_song` records.

**Glossary** — This file; the authoritative vocabulary for the project.

---

## I

**Idempotent** — Safe to run multiple times and yield the same result (e.g.,
upserts by natural key).

**Ingestion** — The process of collecting, parsing, normalizing, and upserting
source data into the database.

**Ingested at** — Timestamp of when a record entered the system (provenance field).

**Issue** — A tracked task/bug/RFC item linked from the schedule.

---

## K

**Knowledge Base (KB)** — Practical hub for sources, recipes, and FAQs
(`docs/knowledge_base.md`).

---

## M

**Materialized view** — A precomputed table of query results to speed up reads.

**MVP** — Minimum Viable Product; the smallest set of features that delivers value
(local‑first, 2020–present).

---

## N

**Natural key** — Real‑world unique identifier used to dedupe and upsert (e.g.,
`(artist_id, date, venue_id)` for a show).

---

## O

**Opener/Closer** — A song appearing at the first or last position of a set.

---

## P

**Pagination** — Splitting API results into pages using `page`/`per_page` or a cursor.

**Personal overlay** — Core stats filtered to a user’s attended shows.

**P95 latency** — The 95th percentile of response times; a performance target.

**Provenance** — Stored lineage fields: `source`, `source_ref`, and `ingested_at`
that explain where data came from and when.

---

## R

**RFC (request for comments)** — A short design decision document under
`docs/decisions/` used for schema/API changes.

**Rolling window** — A time‑bounded slice (e.g., last 365 days) used for stats.

**Runbook** — Operational procedures and troubleshooting guide (`docs/runbook.md`).

---

## S

**Schema** — The structure of tables, columns, constraints, and relationships in
Postgres.

**Segue** — A transition between songs within a set; stored as a boolean flag on
`set_song`.

**Set** — An ordered container of songs within a show; `position` is contiguous per show.

**Set song (`set_song`)** — Join table connecting `set` and `song` with `position`,
`segue`, and notes.

**Show** — A single performance on a date at a venue by an artist; natural key `
(artist_id, date, venue_id)`.

**Source** — The system or site from which data was obtained (provenance field).

**Source ref** — A reference (URL, ID, or hash) for the specific source record.

**Streak** — Consecutive shows for which a song is played or not played.

---

## T

**Token budget (context budget)** — The maximum startup or handoff context allowed for
an agent.

**Tuple** — A specific combination of fields (e.g., a natural key) used to enforce
uniqueness.

---

## U

**Upsert** — Insert or update operation keyed by a natural key to avoid duplicates.

**User** — An authenticated person with attendance and personal stats.

---

## V

**Venue** — A normalized performance location with city, state, and country.

---

## W

**Window** — The date range used for a stat (e.g., rolling_365, year_to_date).

---

## Z

**Zero‑downtime migration** — A schema change strategy that avoids service interruption
(e.g., add column → backfill → swap).

---

### Cross‑References

* System map: `docs/system_overview.md`
* Tables and constraints: `docs/database_schema.md`
* Sources, recipes, queries: `docs/knowledge_base.md`
* Ops: `docs/runbook.md`
