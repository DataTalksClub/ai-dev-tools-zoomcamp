# Article 2: Build and Ship a Full-Stack App with AI Coding Assistants

Locator: `/home/alexey/git/ai-dev-tools-zoomcamp/articles/02-end-to-end.md`

The direct predecessor defines the series voice, the system-design interview
canvas, and the contract for Article 3.

- [FACT article-2-end-to-end] The application has a React frontend, FastAPI
  backend, SQLite persistence through SQLAlchemy, and realtime WebSocket rooms.
- [FACT article-2-end-to-end] The implementation proceeds through replaceable
  layers: mocked frontend service, real backend with in-memory storage, then
  SQLite.
- [FACT article-2-end-to-end] The deployment handoff promises containers,
  full-flow integration tests, CI, Postgres with Compose, migrations, a public
  deployment, and CD.
- [HUMAN] The author prefers short prompts, tests each intermediate result, and
  gives observed failures back to the coding assistant.

Limitation: Article 2 describes a local build and does not prove the later cloud
resources or pipeline.

Captured: 2026-08-09.
