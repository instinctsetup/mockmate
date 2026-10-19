# mockmate

Interview prep, grounded in sources. Company-prep intel and an OA question bank
with source URLs for every claim, plus a mock-interview module. Model-written
answers are always labeled as such.

Status: **WIP scaffold** - backend core first, web UI next.

## Architecture

- **web/** - Next.js (TypeScript) dashboard: company prep, OA bank, mock interviews
- **api/** - FastAPI service: company intel, OA questions, mock sessions
- **Postgres** - companies, questions, sessions
- **Redis** - intel search cache (24h TTL)
- **intel providers** - pluggable search backends behind one interface:
  `fixture` (offline, default for tests/CI) and `duckduckgo` (live).
  No login-walled scraping anywhere.

## Ground rules

- Every intel claim and OA question carries source URLs.
- Model-written answers are labeled `model-written` in the UI and API.
- Fixture mode is the default in tests; live search is opt-in via env.
