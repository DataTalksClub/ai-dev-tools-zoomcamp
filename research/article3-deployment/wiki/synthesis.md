# Synthesis

## Recommended through-line

- [HUMAN] Continue Article 2's interview-canvas example and direct teaching
  voice.
- [INFERENCE article-2-end-to-end,full-stack-workshop-deployment] Preserve the
  same incremental pattern used during development: make one operational change,
  test the resulting artifact, and only then add the next layer.
- [INFERENCE full-stack-workshop-deployment,interview-canvas-repository] Use the
  sequence integration tests → one container → Postgres → Compose → migrations →
  AWS → GitHub Actions → cleanup.

## Required translations

- [FACT interview-canvas-repository] The database setting is
  `SDIP_DATABASE_URL`, not the workshop's `SNAKE_ROYALE_DATABASE_URL`.
- [FACT interview-canvas-repository] The existing multi-stage Dockerfile copies
  `frontend/dist/client` into `app/static` and serves the application on port
  8000.
- [FACT interview-canvas-repository] Backend tests run with `make test`. The
  frontend has lint and build commands but no test command at captured commit
  `80d78eb`, so Article 3 must not imply that a frontend suite already exists.
- [FACT interview-canvas-repository] The application's distinctive deployment
  seam is its authenticated WebSocket room, so a useful integration test must
  involve two clients and a propagated canvas change.
- [INFERENCE article-2-end-to-end,interview-canvas-repository] Commands and
  examples should use names such as `interview-canvas`, `interview-canvas-db`,
  and `sdip`, not `snake-royale` or `snakearena`.

## Workshop material to preserve

- [FACT full-stack-workshop-deployment] The workshop builds the React frontend
  in a Node stage and serves its static output from the Python/FastAPI stage.
- [FACT full-stack-workshop-deployment] It validates persistence first with a
  named SQLite volume, then adds a Postgres driver and runs Postgres locally.
- [FACT full-stack-workshop-deployment] Compose gives the database a stable
  service hostname and uses a health check before starting the app.
- [FACT full-stack-workshop-deployment] The AWS path uses infrastructure as code,
  a managed PostgreSQL database, one VM for the application container, HTTPS,
  and a public URL.
- [FACT full-stack-workshop-deployment] The CI/CD path runs fast frontend and
  backend tests first, integration tests afterward, and deploys only from
  `main`; AWS authentication uses GitHub OIDC instead of a stored access key.
- [FACT full-stack-workshop-deployment] The workshop explicitly removes cloud
  resources afterward because the AWS stack costs money while it is running.

## Material Article 3 must add or correct

- [FACT article-2-end-to-end] Article 2 promised integration tests, Postgres,
  Docker Compose, database migrations, public deployment, and continuous
  delivery.
- [FACT full-stack-workshop-deployment] The workshop deferred database
  migrations. Article 3 should include an Alembic step so the series fulfills
  its stated promise and does not suggest that `create_all()` is a production
  migration strategy.
- [INFERENCE full-stack-workshop-deployment,interview-canvas-repository] The
  first Docker failure should be framed as a general lesson to inspect the
  generated frontend output. For this repository, the verified target is
  `dist/client`; the Snake Royale workaround should not be copied.
- [INFERENCE full-stack-workshop-deployment,interview-canvas-repository] The AWS
  prompt must mention WebSocket support and HTTPS because realtime collaboration
  is central to the deployed application.

## Ending and caveats

- [FACT interview-canvas-repository] The current repository only contains work
  through the single Docker image at commit `80d78eb`; later article sections
  should present reproducible prompts and the intended output, not falsely imply
  those deployment files already exist in the linked repository.
- [FACT full-stack-workshop-deployment] A proof-of-concept deployment still
  needs hardening: restricted CORS, durable authentication, secret storage,
  migrations, health checks, logs, and a rollback path.
- [INFERENCE article-2-end-to-end,full-stack-workshop-deployment] End by pointing
  forward to the DevOps and observability article, where operation after the
  first successful deploy becomes the focus.
