**Quran Link**

A focused full-stack application for Quran memorization practice. It pairs a Vue 3 single-page frontend with a FastAPI backend and offers interactive word-by-word and verse-by-verse testing with selectable ranges (page, juz, or explicit verse ranges).

## Screenshots

### Main Interface
![Main Interface](screenshots/main-interface.png)
*The main testing interface with Arabic text and word-by-word input*

### Dark & Light Themes
<div style="display: flex; gap: 10px;">
  <img src="screenshots/dark-theme.png" alt="Dark Theme" width="48%">
  <img src="screenshots/light-theme.png" alt="Light Theme" width="48%">
</div>

*Support for both dark and light themes with system preference detection*

### Bilingual Support
![Arabic Interface](screenshots/arabic-mode.png)
*Full Arabic interface with RTL support*

---

## Quick Overview
**Backend:** FastAPI JSON API for Surahs and verses backed by a lightweight SQLite store.
**Frontend:** Vue 3 SPA with i18n (Arabic/English), theme support, and interactive memorization exercises.

### Project Structure (high level)
- [server/](server/) — FastAPI backend (see key modules: `app.py`, `modules/`)
- [client/](client/) — Vue 3 frontend (core component: `src/App.vue`)

---

## HTTP API Endpoints

GET `/surahs`
- Returns an array of Surah objects (`id`, `name`, `en_name`, `ayahs_count`).

GET `/verses?range_type=<type>&range_value=<value>`
- `range_type`: `page`, `juz`, or `key`.
- `range_value`: for `page`/`juz` use `start:end` (e.g. `1:3`); for `key` use `surah:ayah-surah:ayah` (e.g. `2:255-2:260`).

GET `/pages?pages=<start:end>`
- Returns verse objects representing page boundaries.

Static files are served from `server/public` at `/`.

---

## Features
- Interactive testing modes: word-level and verse-level.
- Range selection: page, juz, or explicit surah:ayah ranges.
- Bilingual UI with RTL support for Arabic.
- Dark/light theme with persistence.
- Responsive design and toast notifications for feedback.

---

## Project Architecture (brief)

Components (key): `ButtonOptions.vue`, `RangeSelector.vue`, `VerseSelector.vue`, `SurahBorder.vue`, `testVerse.vue`, `testWord.vue`.

State and i18n: see `client/src/store.js` and `client/src/i18n/`.

Storage and models: see `server/modules/engine/db_storage.py`, `server/modules/surahs.py`, and `server/modules/ayahs.py`.

---

## Notes & Troubleshooting
- Database files used by `populat_data.py` are expected under `server/data`.
- The frontend resolves the backend URL from `window.__API_URL__`, then `VUE_APP_API_URL`, then falls back to `http://localhost:8000`.
- CORS is permissive by default for development; review production settings before deployment.

---

# TODOS
- Implemnt a progress save storege to not fetch the defaults on each requets
- Support progress and status sharing

---
