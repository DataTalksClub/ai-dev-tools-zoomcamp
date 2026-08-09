# interview-canvas-share repository

Locator: `https://github.com/alexeygrigorev/interview-canvas-share`

The repository is the source of truth for adapting the workshop to Article 2's
application. Inspected at commit `80d78eb` on 2026-08-09.

- [FACT interview-canvas-repository] The root contains `backend/`, `frontend/`,
  `Dockerfile`, `Makefile`, `openapi.yaml`, and `AGENTS.md`.
- [FACT interview-canvas-repository] `SDIP_DATABASE_URL` configures SQLAlchemy;
  its default is `sqlite:///./sdip.db`.
- [FACT interview-canvas-repository] The Dockerfile uses Node 24 and Python 3.12
  stages, copies `frontend/dist/client` to `app/static`, and exposes port 8000.
- [FACT interview-canvas-repository] The Makefile exposes `make run` and
  `make test` for the backend.
- [FACT interview-canvas-repository] The frontend exposes lint and build
  commands but no test command at the captured commit.
- [FACT interview-canvas-repository] Tests cover authentication, sessions,
  database behavior, static serving, guest/canvas behavior, and realtime
  WebSocket behavior.
- [FACT interview-canvas-repository] No Compose, migrations, CloudFormation, or
  GitHub Actions files exist at this commit.

Limitation: the default branch can change after capture. Later deployment steps
are proposals adapted from the workshop unless the repository adds them.

Captured: 2026-08-09.
