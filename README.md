# SpreadSheetz — Widespread Panic Setlist Stats & Attendance

> **Mission.** A fast, respectful, and community‑minded setlist and attendance tracker for Widespread Panic. **Everyday Companion (EC)** is our primary reference; **TourWrangler (TW)** is secondary. Panicstream is out‑of‑scope.

**Status:** MVP in progress · **Last Updated:** 2025‑11‑06

---

## Contributor Guide

> For a complete guide on how to contribute to this project, including setup, development standards, and architectural overview, please see our primary contributor guide:
> 
> **[➡️ CONTRIBUTING.md](CONTRIBUTING.md)**

---

## Quickstart

```bash
# 1) Clone & set up
uv sync  # or: pip install -r requirements.txt

# 2) Environment
cp .env.example .env  # add DB creds

# 3) Dev services
docker compose up -d  # postgres, adminer

# 4) Run API/UI (examples)
uv run api/main.py      # FastAPI (or your chosen stack)
uv run web/dev_server   # React/Vite (optional)
```

### Seed & Smoke Tests

```bash
uv run scripts/seed_demo.py    # songs/venues/shows sample
uv run tests -k smoke          # /shows & /stats perf smoke
```

---

## Data & Provenance (EC/TW)

* **Primary vs secondary:** Prefer **EC** when sources disagree; use **TW** when EC is silent and mark `data_confidence='medium'` until corroborated.
* **Attribution:** Every show stores `show_source(source_id, source_url)` and the UI displays a source pill on show pages.
* **Ethics:** Respect robots/ToS. Rate limits and ingestion rules live in **docs/knowledge_base.md**.

**Start here:**

* 📚 **Knowledge Base** → EC/TW mapping tables, rate limits, conflict resolution.
* 🗄️ **Database Schema** → canonical tables + Phase‑2 entities (tease/guest/performance_tag).
* 📝 **Corrections Policy** → end‑to‑end curator workflow & SLAs.

---

## API Overview (preview)

* `GET /shows` — list/filter shows; includes provenance and `data_confidence`.
* `GET /shows/{id}` — details with sets/songs; includes **jams**, **teases**, and **guests** (Phase‑2).
* `GET /songs/{id}/teases` — performances that tease a given song.
* `POST /corrections` — create an intake ticket (public; rate‑limited).
  **Full contract:** see **docs/system_overview.md** and **docs/database_schema.md**.

---

## Contributing

* Open an issue with a clear **What/Why/How** and link the schedule item.
* Keep PRs small; update docs in the same PR or a linked follow‑up.
* For data corrections, follow **docs/corrections_policy.md**.

---

## Change Log

* **2025‑11‑06:** Wired cross‑links to **Knowledge Base (EC/TW)**, **Database Schema (Phase‑2)**, and **Corrections Policy**. Clarified data/provenance rules and read‑first path.
