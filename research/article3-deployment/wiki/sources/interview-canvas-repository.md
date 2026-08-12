# interview-canvas-share repository

Locator: `https://github.com/alexeygrigorev/interview-canvas-share`

The repository is the source of truth for the post-workshop implementation.
Inspected at commit `e536482` on 2026-08-12.

- [FACT interview-canvas-repository] The root contains `backend/`, `frontend/`,
  `Dockerfile`, `Makefile`, `openapi.yaml`, and `AGENTS.md`.
- [FACT interview-canvas-repository] `SDIP_DATABASE_URL` configures SQLAlchemy;
  its default is `sqlite:///./sdip.db`.
- [FACT interview-canvas-repository] The Dockerfile uses Node 24 and Python 3.12
  stages, copies `frontend/dist/client` to `app/static`, and exposes port 8000.
- [FACT interview-canvas-repository] The Makefile exposes `make run` and
  `make test` for the backend, plus Compose, integration, frontend, and
  Playwright test targets.
- [FACT interview-canvas-repository] `docker-compose.yaml` runs the app and
  Postgres, waits for the database health check, and publishes the app on port
  8100 by default.
- [FACT interview-canvas-repository] Integration tests exercise HTTP and
  WebSocket behavior against the deployed stack. Playwright reproduces the
  interviewer and candidate flow in two browser contexts.
- [FACT interview-canvas-repository] `deploy/aws/sdip-stack.yaml` deploys one
  EC2 instance and supports either Caddy with a domain or CloudFront without a
  domain. Postgres remains on the instance volume.
- [FACT interview-canvas-repository] `.github/workflows/ci.yml` runs backend
  and frontend jobs in parallel, then integration and end-to-end tests, then a
  deployment through a restricted AWS Systems Manager document and OIDC role.

Limitation: the default branch can change after capture. The AWS deployment is
a single-instance proof of concept, not a managed or highly available setup.

Captured: 2026-08-12.
