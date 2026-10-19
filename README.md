# mockmate

Interview prep, grounded in sources. Company-prep intel and an OA question
bank where **every item carries a source URL and every model-written answer is
labeled as one** - plus practice-session logging.

- **Demo video**: https://drive.google.com/file/d/16ELJeiM3hAnckwhd2OgwmAasvK0jLtk2/view
- **Project report (PDF)**: https://drive.google.com/file/d/1WApCYVpfEfxf9i_cClhRB4jIu1cb8CbH/view
- Repo: https://github.com/instinctsetup/mockmate

## What it does

- **Company prep** (`/api/prep/{company}`): interview intel from pluggable
  search providers + the OA questions community-tagged for that company.
- **OA question bank**: 15 seeded real problems with canonical source URLs,
  topic/difficulty/company filters, and solutions that are model-written and
  labeled `model_written` in both API and UI.
- **Practice sessions**: log what you practiced; stored in Postgres.
- **Honesty by schema**: company tags are labeled community-reported, not
  verified; intel items always carry `url` + `source`; the provider name is
  returned with every search.

## Architecture

```
web/   Next.js 14 (App Router, strict TypeScript) - company prep, OA bank, session logging
api/   FastAPI - /api/prep, /api/oa/questions, /api/intel/search, /api/sessions, /api/health
db     Postgres 16 (sessions) - in-memory fallback when DATABASE_URL is absent/unreachable
cache  Redis 7 (24h intel cache) - in-process fallback when REDIS_URL is absent/unreachable
intel  pluggable SearchProvider: fixture (offline, default) | duckduckgo (live, no login walls)
```

## Quickstart

```bash
docker compose up            # api on :8101 with Postgres + Redis
cd web && npm install && npm run dev   # UI on :3100
```

Or without Docker (fallback mode, everything still works):

```bash
pip install -r api/requirements.txt
cd api && uvicorn app.main:app --port 8101
cd ../web && npm install && npm run dev
```

Live search is opt-in: `MOCKMATE_SEARCH=duckduckgo` (default is the offline
fixture provider, which tests and CI use).

## Tests

```bash
python3 -m pytest tests/ -q     # 9 tests: providers, OA bank, API, fallbacks
cd web && npx tsc --noEmit      # strict typecheck (also in CI)
```

CI runs both on every push.

## Honest limitations

- The bank is a 15-question seed; the schema/API are built to grow with sourced entries.
- Company tags are community-reported, never presented as verified.
- The live DuckDuckGo provider parses public HTML and can break with upstream
  changes; fixture mode keeps the app independent of it.
- No auth; single-user by design.
