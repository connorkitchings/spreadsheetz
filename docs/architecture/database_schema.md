# Database Schema — SpreadSheetz Setlist Platform

> **Purpose.** Single source of truth for entities, relationships, and constraints that power Widespread Panic setlists and personal attendance features. This revision focuses on **Phase‑2 support for teases, guests, and jam flags**, aligned to our source policy (Everyday Companion primary; TourWrangler secondary).

**Notation.** `snake_case` for columns; PostgreSQL; `id` columns are ULIDs; timestamps are UTC `timestamptz`.

---

## 0) High‑Level Entity Map

```
artist 1—* show *—* set 1—* set_song *—1 song
                 |                     \
                 |                      \— performance_tag (Phase‑2)
                 |\
                 | \— show_source (EC/TW provenance)
                  \
                   \— show_guest (Phase‑2 guest appearances)

set_song — tease (Phase‑2, links to teased song)
```

---

## 1) Core Tables (Phase‑1)

### 1.1 artist

* `id` ULID PK
* `slug` text UNIQUE (e.g., `wsp`)
* `name` text NOT NULL

### 1.2 venue

* `id` ULID PK
* `name` text NOT NULL
* `city` text NOT NULL
* `region_code` text NULL (e.g., `CO`)
* `country_code` char(2) NOT NULL DEFAULT 'US'
* Index: `(name, city, region_code, country_code)`

### 1.3 venue_alias

* `alias` text NOT NULL
* `venue_id` ULID FK → venue(id)
* `valid_from` date NULL, `valid_to` date NULL (handle renames)
* Unique: `(alias, venue_id, coalesce(valid_from,'-inf'), coalesce(valid_to,'+inf'))`

### 1.4 show

* `id` ULID PK
* `artist_id` ULID FK → artist(id)
* `show_date` date NOT NULL
* `venue_id` ULID FK → venue(id)
* `city` text NOT NULL
* `region_code` text NULL
* `country_code` char(2) NOT NULL DEFAULT 'US'
* `data_confidence` text NOT NULL DEFAULT 'high' CHECK in('low','medium','high')
* Unique: `(artist_id, show_date, venue_id)`
* Index: `(artist_id, show_date)`

### 1.5 show_source (provenance)

* `show_id` ULID FK → show(id)
* `source_id` text NOT NULL CHECK in('ec','tw')
* `source_url` text NOT NULL
* `first_seen_at` timestamptz NOT NULL DEFAULT now()
* PK: `(show_id, source_id)`

### 1.6 set

* `id` ULID PK
* `show_id` ULID FK → show(id)
* `set_order` int NOT NULL (1..N)
* `is_encore` boolean NOT NULL DEFAULT false
* `encore_order` int NULL (1..N when `is_encore`)
* Unique: `(show_id, set_order)`

### 1.7 song

* `id` ULID PK
* `name` text NOT NULL UNIQUE (canonical)
* `aka` jsonb NULL (alias list)

### 1.8 set_song (performance row)

* `id` ULID PK
* `set_id` ULID FK → set(id)
* `song_id` ULID FK → song(id)
* `song_position` int NOT NULL (1‑based per set)
* `segue_next` boolean NOT NULL DEFAULT false
* `segue_symbol` text NULL CHECK in('>','→','->')
* **Phase‑2 columns added:**

  * `is_jam` boolean NOT NULL DEFAULT false
  * `jam_minutes` numeric(4,1) NULL CHECK (jam_minutes >= 0)
* Unique: `(set_id, song_position)`

---

## 2) Phase‑2 Feature Tables (New)

### 2.1 guest (canonical)

* `id` ULID PK
* `name` text NOT NULL UNIQUE (e.g., `John Keane`)
* `primary_instrument` text NULL (free text: `guitar`, `pedal steel`)
* `aka` jsonb NULL (alias list)

### 2.2 show_guest (appearance at show level)

* `id` ULID PK
* `show_id` ULID FK → show(id) ON DELETE CASCADE
* `guest_id` ULID FK → guest(id)
* `instruments` text[] NULL (override/augment `primary_instrument`)
* `notes` text NULL (e.g., `appears only on set II`)
* Unique: `(show_id, guest_id)`

> **Why show‑level?** Some sources only say "with X" without specifying songs. When songs are known, we also link at `set_song` level via `performance_tag` rows (type `guest_on_song`).

### 2.3 tease (links a performance to a different canonical song)

* `id` ULID PK
* `set_song_id` ULID FK → set_song(id) ON DELETE CASCADE
* `teased_song_id` ULID FK → song(id)
* `confidence` text NOT NULL DEFAULT 'high' CHECK in('low','medium','high')
* `note` text NULL (free‑form, e.g., lyric snippet)
* `source_id` text NOT NULL CHECK in('ec','tw')
* `source_url` text NOT NULL
* Unique: `(set_song_id, teased_song_id, source_id)`

### 2.4 performance_tag (flexible, for jams/guests/bustouts)

* `id` ULID PK
* `set_song_id` ULID FK → set_song(id) ON DELETE CASCADE
* `tag_type` text NOT NULL CHECK in('jam','guest_on_song','bustout','rare','disputed')
* `value` jsonb NULL (e.g., `{ "length_min": 12.5 }` or `{ "guest_id": "01H..." }`)
* `source_id` text NOT NULL CHECK in('ec','tw','curator')
* `source_url` text NULL
* Index: `(tag_type, set_song_id)`

### 2.5 annotation (free‑form per show/set/song)

* `id` ULID PK
* `show_id` ULID NULL FK → show(id)
* `set_id` ULID NULL FK → set(id)
* `set_song_id` ULID NULL FK → set_song(id)
* `type` text NOT NULL CHECK in('note','disputed','correction')
* `body` text NOT NULL
* `source_id` text NOT NULL CHECK in('ec','tw','curator','user')
* `source_url` text NULL
* **Scope rule:** exactly one of (`show_id`,`set_id`,`set_song_id`) must be non‑NULL.

---

## 3) Parsing & Ingestion Contracts (EC/TW)

* **Guests**

  * If page says `with John Keane`, create `guest` (if new), add `show_guest` row.
  * If specific songs noted (`Surprise Valley (with JK)`), also create `performance_tag` on the corresponding `set_song` with `tag_type='guest_on_song'` and `value={"guest_id": ..., "instrument": "guitar"}`.
* **Teases**

  * Inline markers like `[Tease: Low Spark]` → insert `tease(set_song_id, teased_song_id)`.
  * When only free‑text appears, map via best alias match; if unresolved, add `annotation(type='note')` and `confidence='medium'`.
* **Jams**

  * Bracketed lengths like `(> Jam 10:30)` or known jam sections → set `set_song.is_jam=true` and `jam_minutes`. If jam is an inserted segment rather than the song itself, add `performance_tag` with `tag_type='jam'` and a `value` length.

---

## 4) Constraints & Data Integrity

* `set_song` must reference existing `song_id`; alias resolution happens upstream during ingestion (see Knowledge Base).
* `tease.teased_song_id` must be a valid canonical song.
* `performance_tag.value` is schema‑light; validators enforce required keys for each `tag_type` in application layer.
* `show_source` must exist for every `show` with at least one source row.

---

## 5) Indices & Performance

* `set_song(set_id, song_position)` UNIQUE (already defined)
* `tease(set_song_id)` and `tease(teased_song_id)` BTREE
* `performance_tag(tag_type, set_song_id)` BTREE
* `show(show_date)` BTREE; partial index: `WHERE data_confidence <> 'high'` for curator queues

---

## 6) Example Queries

**A) All teases of “Low Spark” in 2011**

```sql
SELECT s.show_date, v.city, v.region_code, so.name AS performed,
       ts.name AS teased
FROM tease t
JOIN set_song ss ON ss.id = t.set_song_id
JOIN set se ON se.id = ss.set_id
JOIN show s ON s.id = se.show_id
JOIN venue v ON v.id = s.venue_id
JOIN song so ON so.id = ss.song_id
JOIN song ts ON ts.id = t.teased_song_id
WHERE ts.name = 'Low Spark of High Heeled Boys'
  AND EXTRACT(YEAR FROM s.show_date) = 2011
ORDER BY s.show_date;
```

**B) Songs with guest sit‑ins over time**

```sql
SELECT so.name, date_trunc('year', s.show_date) AS yr, count(*) AS appearances
FROM performance_tag pt
JOIN set_song ss ON ss.id = pt.set_song_id
JOIN set se ON se.id = ss.set_id
JOIN show s ON s.id = se.show_id
JOIN song so ON so.id = ss.song_id
WHERE pt.tag_type = 'guest_on_song'
GROUP BY 1,2
ORDER BY 2,3 DESC;
```

**C) Long jams leaderboard (≥ 10 min)**

```sql
SELECT s.show_date, v.city, v.region_code, so.name, ss.jam_minutes
FROM set_song ss
JOIN set se ON se.id = ss.set_id
JOIN show s ON s.id = se.show_id
JOIN venue v ON v.id = s.venue_id
JOIN song so ON so.id = ss.song_id
WHERE ss.is_jam = true AND ss.jam_minutes >= 10
ORDER BY ss.jam_minutes DESC
LIMIT 50;
```

---

## 7) Migration Plan (Phase‑2)

1. Create new tables: `guest`, `show_guest`, `tease`, `performance_tag`, `annotation`.
2. Add columns to `set_song`: `is_jam boolean`, `jam_minutes numeric(4,1)`.
3. Backfill provenance: ensure every existing `show` has at least one `show_source` row.
4. Write ingestion updates:

   * Guest parsing → create `guest/show_guest` and `performance_tag` as needed.
   * Tease parsing → create `tease` links; unresolved → `annotation`.
   * Jam parsing → set flags/lengths.
5. Add curator dashboards for:

   * Unresolved aliases, `confidence != 'high'`, and `annotation.type='disputed'`.

---

## 8) API Touchpoints (FYI)

* `GET /shows/{id}` → include `guests` (from `show_guest`) and summary counts (`teases`, `jams`).
* `GET /shows/{id}/setlist` → include `set_song` with `is_jam`, `jam_minutes` and nested arrays: `teases[]`, `tags[]`.
* `GET /songs/{id}/teases` → list performances that tease this song.

---

## 9) Glossary (Schema‑specific)

* **Tease:** recognizable reference to another canonical song during a performance.
* **Jam:** extended improvisational segment; may be part of a song or standalone; we model at `set_song` level.
* **Guest:** non‑band musician appearing at a show; may appear at show level or per‑song.

---

## 10) Change Log (this file)

* **2025‑11‑06:** Added Phase‑2 tables (`guest`, `show_guest`, `tease`, `performance_tag`, `annotation`) and jam flags on `set_song`. Included parsing contracts, indices, queries, and migration plan.
