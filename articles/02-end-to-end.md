# Build and Ship a Full-Stack App with AI Coding Assistants

This is the second article in a series based on
[AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp),
the free course we run at DataTalks.Club.

The [first one](https://alexeyondata.substack.com/p/ai-native-development-specifications)
was about the workflow: specifications, context, and a team of agents
working through a backlog. This one is about what that workflow
produces - one app, from an empty repo to a public URL, with a
database, tests, containers, and a pipeline that deploys on every push.

This is a stripped-down version of a full-day workshop,
[Build and Deploy a Full-Stack App with AI Coding Assistants](https://aishippinglabs.com/workshops/full-stack-vibe-coding).
Here I keep the prompts and the reasoning behind them, and skip the
step-by-step. The finished app is
[snake-royale](https://github.com/alexeygrigorev/snake-royale).

We build the classic Snake game, made multi-user: a leaderboard, a page
for watching other people's games, and login. React on the front,
FastAPI on the back, one container serving both.

We won't write much of it ourselves. Every step is a prompt to a coding
assistant. I use [Codex](https://developers.openai.com/codex/), but the
prompts are plain English and work the same in Claude Code, Copilot,
Cursor, or Antigravity.


## The order

The stack matters less than the order we build in:

1. The frontend, running on a fake backend.
2. An OpenAPI spec, derived from what that frontend calls.
3. The backend, generated from the spec.
4. Then persistence, containers, deployment, pipeline.

Each step hands the next one a precise target instead of a guess. This
is the same idea as the first article - specify, then build - applied
to a whole app rather than one task.


## Frontend first

We start with the UI because it's the part we can judge by looking at
it. Once it runs, it tells us what the backend has to support.

I use [Lovable](https://lovable.dev/), which generates a React app from
one prompt. v0, Bolt, or a coding assistant writing React directly all
work.

```text
Create an interactive Snake game with two modes:

- walls (you die hitting a wall)
- pass-through (you wrap around the edges)

Make it multi-user. Add

- a leaderboard showing top scores per mode
- a page to watch other players' active games
- login and signup screens

Centralize every backend call in one services layer, and create a mock
implementation of it so the whole app runs without a real backend.

Add tests.
```

The last two paragraphs are the ones people skip, and they're the ones
that make the rest work.

One services layer means every backend call lives in one place, so
switching from fake to real later is a one-line change. A mock
implementation means the app runs before the backend exists - we can
play the game, submit a score, and sign up while the server is still
hypothetical.

Ask for both explicitly, whatever tool you use.

What comes back has a `services/` folder with `mock.ts`, `http.ts`, and
an `index.ts` that picks between them. Right now it points at the mock.

Get the code out of the generator and into GitHub early, run it
locally, and commit at the end of every step. When the assistant takes
a wrong turn - and it will, around the Docker part - you want a working
commit to go back to.


## Give the assistant the house rules

Assistants guess at the tools we use, and the guesses aren't always
right. Ours would reach for pip, write a `requirements.txt` we don't
want, and install packages into the global Python.

An `AGENTS.md` at the repo root fixes that. The assistant reads it on
startup, from anywhere in the project:

```text
for backend, use uv for dependency management. a few useful commands:

uv sync
uv add <PACKAGE-NAME>
uv run python <PYTHON-FILE>

regularly commit code to git
```

It starts short and grows. Watch for the assistant repeating a mistake
or hunting for something it should already know, and write the answer
down.


## The spec between the two sides

The services layer already lists every call the UI makes. Before
building anything that answers them, we write them down:

```text
Read the frontend's API client in frontend/

Create openapi.yaml at the repo root that specifies the backend this frontend
expects: every endpoint, method, path, request body, response body, and which
endpoints need authentication
```

You can skip this step. I wouldn't. It takes a few minutes and pays
back three times:

- The backend gets a precise target instead of being inferred from
  frontend code.
- We can argue about the API while it's still cheap to change, before
  anything depends on it.
- Every later disagreement between the two sides has one document that
  settles it.

It also saves tokens. When we change an endpoint, the assistant reads
the agreed spec instead of reverse-engineering the frontend again.


## The backend from the spec

We start with an in-memory store, not a database. The first thing worth
proving is that the two sides can talk. A database at this point is one
more thing that can be wrong.

```text
Build a FastAPI backend in backend/ that implements the openapi.yaml spec

Use an in-memory store for now (no database yet) and seed it
with a few fake users, scores, and active games so the frontend has something
to show

Add authentication with hashed passwords and bearer tokens for the
endpoints that need it

Split the code into modules - routers, models, store, auth

Write tests
```

FastAPI publishes interactive docs at `/docs`, generated from the
routes that actually exist. Diffing that against `openapi.yaml`
confirms the backend implements the API we agreed on. From here the
running app is the ground truth.


## Connecting them

The switch is anticlimactic, which is the point of having asked for a
services layer:

```text
Switch the frontend to use the real backend client
```

**Expect to debug here.** This is where the two sides disagree, and
it's normal: a field named differently on each side, a 422 from a
request body that doesn't match, a missing trailing slash. Read the
error in the browser console or the server log, hand it to the
assistant, and ask for the fix. When they disagree, let `openapi.yaml`
settle it and change whichever one diverged.

Somewhere around here, collect the commands into a `Makefile` -
install, run each side, run each test suite. Keeping the test targets
separate matters later, when the pipeline runs them as separate jobs.


## Persistence

Every restart still wipes the accounts and scores.

```text
Replace the in-memory store with a database. Use SQLite and SQLAlchemy

Use an environment variable to configure which DB the server should connect to

Make it database-agnostic - later we will add support for other databases (e.g. postgres)
```

The last two lines are the whole trick. Three steps later, moving to
Postgres is adding a driver and changing one environment variable -
no code change. Cheap instructions when you ask for them, expensive
when you don't.

Then a second test suite, because the existing ones don't cover what
just changed:

```text
Add integration tests in a tests_integration/ folder that run against a
temporary SQLite database

They should exercise full flows:

- sign up
- log in
- submit a score
- read it back from the leaderboard
```

The unit tests are fast and isolated, and they prove a single request
behaves. They don't prove the app works when data has to survive across
separate database connections - which is exactly what was broken when
the store was in memory. Fast tests first, slow ones after.


## Containers

We want one image with the backend and the compiled frontend, so
there's a single thing to build, run, and ship:

```text
Create a Dockerfile that builds the frontend with Node, then builds a Python
image with backend with frontend static files. Backend should serve the frontend.
```

This is where the workshop went wrong, and it's the most useful part of
it. The frontend framework's build produces a server bundle, not the
static files we assumed, so the first image doesn't work. In the live
session a participant who does frontend for a living spotted it: we
need the static build, not the server one.

Given that hint, the assistant adds a prerender step, points the
backend at the output, then installs Playwright and clicks through the
running container to confirm the app loads.

You don't need to understand that framework's build to get past this,
and neither did we. What matters is the loop: the first attempt fails,
you feed back the error and what you know, and it converges. Knowing
enough to say "that's a server bundle, not a static build" is the part
that stays yours.

Then Postgres and Compose, which are short because of the groundwork:

```text
Write a compose.yaml with a postgres service and the app service built from
the Dockerfile

Give Postgres a named volume so data survives

Make the app wait for Postgres to be ready
```

`docker compose up --build` and the full stack runs. If you stop here
you have a complete app - frontend, backend, database, tests,
containers. Everything after is about putting it somewhere public.


## Deploying it

A managed host is the quickest way to a public URL for a proof of
concept. We tried that first, hit free-tier restarts, and moved to AWS:
Aurora Serverless for the database, a single EC2 instance for the
container.

The fundamental here isn't AWS. It's that the infrastructure gets
written down as code rather than clicked together:

```text
Create a CloudFormation template that deploys this app to AWS, with:

- an Aurora PostgreSQL (Serverless v2) database
- the database user and password stored in Secrets Manager
- a single EC2 instance that reads those secrets at boot, builds the image, and
  runs the container with docker
- a public URL for the app
- an idempotent deploy: re-running it must not rotate the secrets
```

Terraform, CDK, and Pulumi do the same job. What you get either way is
a deployment you can re-run, review, and delete in one command - and
you will want to delete it, because a stack like this runs to a couple
of dollars a day.


## The pipeline, and taking the keys away

Deploying by hand works. Across several projects, remembering the exact
steps for this one doesn't.

There's a second reason, specific to building this way. Once you're
past the proof of concept, you don't want agents reaching into your
cloud account. You can't be sure what they'll do there - dropping the
database, for one. Experiment with the infrastructure early, work it
out, then take that access away and let the agents ship only through
CI/CD.

```text
Create a GitHub Actions workflow.

- first run frontend and backend tests in parallel
- then backend integration tests
- then deploy

For deployment, authenticate with OIDC - don't create a user.
```

Fast tests in parallel, integration tests once they pass, deploy only
after that and only on `main`. OIDC means the pipeline authenticates
with short-lived credentials, so no long-lived key sits in the repo.

Once it runs, delete the admin key you used for the first deploy.


## What we left out

A day-long build means taking the simplest option at several points. In
rough order of when it starts to matter: restrict CORS to your own
domain, persist sessions so redeploys don't log everyone out, add
migrations before the schema changes under live data, move to a managed
database and container host, and replace polling with WebSockets if you
want spectating to be live.

Each one is a good next prompt. Same workflow: say what you want, name
the file, read the result against what you know.


## What changes after the first version

We drove all of this one prompt at a time. That's the right speed for
going from nothing to a first version, and it stops being the right
speed shortly after.

Once the codebase is real and growing, ad-hoc prompting drifts. The
assistant forgets earlier decisions, skips tests, and calls work done
too early. What replaces it is the workflow from the
[first article](https://alexeyondata.substack.com/p/ai-native-development-specifications):
each change written down before anyone builds it, and separate agents
for grooming, implementing, and verifying, so nothing grades its own
work.

The material for that is already here. `openapi.yaml` specifies the
API, the two test suites turn acceptance criteria into checks, and the
pipeline ships whatever passes. A new feature extends the spec first,
and the code follows.


## Next in the series

The remaining modules build on the same app:

- Coding agent capabilities: MCP, skills, plugins, hooks and custom
  agents
- AI for security, audit and DevOps
- Taking a project of your own from an empty folder to something
  running

If you'd rather do the course than read it, the materials, the homework
and the next cohort are here:
[AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp).
It's free.

The full workshop, with every step written out, is
[Build and Deploy a Full-Stack App with AI Coding Assistants](https://aishippinglabs.com/workshops/full-stack-vibe-coding).
