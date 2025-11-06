# System Overview — Architecture, UI, and API

> **Purpose.** High‑level blueprint for how SpreadSheetz works across ingestion, storage, API, and UI. This revision adds **EC/TW attribution in UI**, **Phase‑2 entities (teases/guests/jams)**, and **API endpoints** that expose them.

**Last Updated:** 2025‑11‑06
**Sources Policy:** Everyday Companion (**EC**) primary; TourWrangler (**TW**) secondary; Panicstream excluded.

---

## 1) Architecture at a Glance

```
[ EC ]      [ TW ]
  |           |
  |  parsers  |   (rate‑limited, respectful)
  v           v
[ Ingestion Jobs ]  →  [ Staging Tables ]  →  [ Canonical DB ]
                              |                     |
                              |                     ├─ show / set / set_song / song / venue
                              |                     ├─ show_source (provenance)
                              |                     ├─ guest / show_guest (Phase‑2)
                              |                     ├─ tease (Phase‑2)
                              |                     └─ performance_tag / annotation (Phase‑2)
                              |
                              └─ Validators (aliases, order, confidence)

[ API ]  →  [ Web UI ]  →  [ Users / Curators ]
```

---

## 2) UI Overview

### 2.1 Show Page

* **Header**: Artist, date, city, venue.
* **Source pill**: "Source: EC" or "Source: TW" (link to `source_url`). Multiple sources list as compact chips.
* **Confidence**: Show `data_confidence` as a subtle badge (High / Medium / Low).
* **Disputed banner**: If any `annotation(type='disputed')` exists for this show, show a dismissible banner summarizing the dispute and linking to details.
* **Setlist**: Render sets with song order, segues (`>`, `→`, `->`).
* **Phase‑2 details**:

  * **Jams**: Show clock icon with `jam_minutes` where `is_jam=true`.
  * **Teases**: Inline bracket link (e.g., `[Low Spark tease]`) linking to song details.
  * **Guests**: Per‑song inline chips when available; otherwise a show‑level "Guests" panel from `show_guest`.
* **Suggest a correction** button: opens intake form (ties to Corrections Policy).

### 2.2 Song Detail Page

* Play count, last played, avg gap.
* **Teased‑by** list: performances where this song was teased (`GET /songs/{id}/teases`).
* **With guests**: top guest collaborators via `performance_tag(tag_type='guest_on_song')`.

### 2.3 Lists & Search

* Server‑side filters for date range, city/venue, has‑teases, has‑guest, min jam length.
* Each result row displays **source chips** and **confidence badge**.

---

## 3) API Surface (stable preview)

Base path: `/api/v1`

### 3.1 Shows

* `GET /shows`

  * **Query params**: `date_from`, `date_to`, `city`, `venue_id`, `has_tease` (bool), `has_guest` (bool), `min_jam_min` (float), `confidence` (one of `high|medium|low`), `page`, `page_size`.
  * **Returns**: paginated list with `id`, `artist_id`, `show_date`, `venue{}`, `data_confidence`, `sources[]`.

* `GET /shows/{id}`

  * **Returns**: show meta; `sources[]`; `annotations[] (type='disputed'|...)`; sets with songs including `segue_next`, `is_jam`, `jam_minutes`; nested `teases[]` and `tags[]`; `guests[]` (show level).

### 3.2 Songs

* `GET /songs/{id}`: canonical song details + usage stats snapshot.
* `GET /songs/{id}/teases`: all performances where this song was teased (joins `tease` → `set_song`).

### 3.3 Corrections

* `POST /corrections`: public intake (rate‑limited). Payload references our app URL and EC/TW links.
* `GET /shows/{id}/history`: audit trail from `audit_log` (latest 50).

**Errors** (shared envelope):

```json
{ "error": { "code": "bad_request", "message": "...", "details": { } } }
```

**Pagination**: cursor or page/size (define in api_contract when stabilized).

---

## 4) Data Model Highlights

* **Provenance**: `show_source(show_id, source_id in ['ec','tw'], source_url)`; every show must have ≥ 1 row.
* **Confidence**: `show.data_confidence in ('low','medium','high')` with curator rules from Corrections Policy.
* **Phase‑2**:

  * `set_song.is_jam`, `set_song.jam_minutes`
  * `tease(set_song_id, teased_song_id, confidence, source_id, source_url)`
  * `performance_tag(tag_type in ['jam','guest_on_song','bustout','rare','disputed'], value jsonb)`
  * `guest`, `show_guest`

---

## 5) Ingestion & Freshness

* **Active tour**: TW daily; EC every 3 days.
* **Off‑tour**: Weekly checks for retro edits.
* **Backfill**: Weekly for 6 weeks post‑show if any page is provisional or partial.
* **Ethics**: Honor robots/ToS; conservative rate limits (see Knowledge Base).

---

## 6) Observability & SLOs

* **API**: P95 < 200 ms on `/shows` index with warm cache; P95 < 300 ms on `/shows/{id}`.
* **Jobs**: < 1% parser failure rate; alert on alias drift (`song_pending` growth > 0.1%).
* **UX**: Time‑to‑interactive on show page < 1.5s on broadband.

---

## 7) Security Notes (quick)

* Secrets via env; no secrets committed.
* Rate limit `POST /corrections` per IP; captcha as needed.
* Least‑privileged DB roles for ingestion vs API.

---

## 8) Open TODOs

* Finalize `api_contract.md` with response schemas.
* Add cache keys for `/shows` list/detail including `confidence`.
* Curator dashboard for disputes and alias review.

---

## 9) Change Log (this file)

* **2025‑11‑06:** Added UI source pill, disputed banner, Phase‑2 entities in data model, and API endpoints to surface teases/guests/jams. Clarified ingestion cadence and SLOs.
