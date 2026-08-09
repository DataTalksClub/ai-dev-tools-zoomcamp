# Containerize and Deploy a Full-Stack App with AI Coding Assistants

This is the third article in a series for [AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp),
the free course we run at DataTalks.Club.

In the [previous article](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/articles/02-end-to-end.md),
we built an application for system-design interviews. An interviewer creates a
session and shares a link with a candidate. Both people work on the same canvas,
and FastAPI sends their changes through WebSockets. We use SQLAlchemy with
SQLite to keep the data after a restart.

You can find the code in the
[interview-canvas-share](https://github.com/alexeygrigorev/interview-canvas-share)
repository.

The application works locally, but other people can't use it yet. We'll first
package the frontend and backend into one container. Then we'll switch to
Postgres and add Docker Compose, integration tests, AWS deployment, and GitHub
Actions.

I'm adapting the deployment half of my AI Shipping Labs workshop,
[Build and Deploy a Full-Stack App with AI Coding Assistants](https://aishippinglabs.com/workshops/full-stack-vibe-coding).
In the workshop, I cover every step in more detail.

## Containerization

Running the application locally requires two commands. We start Vite for the
frontend and uvicorn for the backend. For deployment, I want one image that
contains the FastAPI backend and the compiled frontend.

We build the React application into static files during the first Docker stage.
The second stage installs the Python dependencies, copies those static files
into the backend, and starts uvicorn. FastAPI then serves both the API and the
frontend on port 8000.

Ask the coding assistant to create it:

```text
Create a multi-stage Dockerfile at the repository root.

Build the frontend with Node. Then create a Python image for the FastAPI
backend, copy the compiled frontend into the backend's static directory, and
serve both from uvicorn on port 8000.

Use uv to install the backend dependencies. Add a .dockerignore.

Build the image, run it, and verify the frontend, /docs, /health, and the
WebSocket connection through the public port.
```

The first image didn't work because it copied the wrong frontend output. The
frontend tooling produced several build directories, and the assistant assumed
the backend should serve the server bundle.

I asked it to look at the result of `npm run build`, which puts this
application's browser files in `frontend/dist/client`. The final Dockerfile
copies that directory into `app/static` in the Python image. You can see the
finished [Dockerfile](https://github.com/alexeygrigorev/interview-canvas-share/blob/main/Dockerfile)
in the application repository.

Coding assistants often get this boundary wrong. You don't need to know every
frontend build tool in advance. You need to look at the build output and test
the image through its exposed port.

Build the image from the repository root:

```bash
docker build -t interview-canvas .
```

Run it with the SQLite database on a named volume:

```bash
docker run --rm \
  -p 8000:8000 \
  -e SDIP_DATABASE_URL="sqlite:////data/sdip.db" \
  -e SDIP_JWT_SECRET="local-container-secret" \
  -v interview-canvas-data:/data \
  interview-canvas
```

At [localhost:8000](http://localhost:8000), use the seeded interviewer and create
an interview session. Then open the join link in a private browser window, move
an element on the candidate canvas, and check that the interviewer sees the
change.

Stop the container and run it again. The named volume keeps `sdip.db`, so the
interview session should still exist.

## Switch from SQLite to Postgres

SQLite needs no separate server, so we use it while we develop locally. For
deployment, we'll use Postgres. In Article 2, we put all database access behind SQLAlchemy and the
`SDIP_DATABASE_URL` environment variable, so we don't need to rewrite the store.
We only add a Postgres driver and test the same code against another database.

Start Postgres locally:

```bash
docker run -d \
  --name interview-canvas-db \
  -e POSTGRES_USER=sdip \
  -e POSTGRES_PASSWORD=sdip \
  -e POSTGRES_DB=sdip \
  -p 5432:5432 \
  -v interview-canvas-pgdata:/var/lib/postgresql/data \
  postgres:16-alpine
```

Use the `sdip` password only for local development, and don't use it for a
public database.

Now give the assistant a bounded task:

```text
Add Postgres support to the backend.

Keep SQLite support for local development and tests. Add psycopg so SQLAlchemy
can connect to Postgres through SDIP_DATABASE_URL.

Run the backend against the local Postgres container and run all backend tests.
```

Point the backend at Postgres and start it:

```bash
export SDIP_DATABASE_URL="postgresql+psycopg://sdip:sdip@localhost:5432/sdip"
make run
```

Repeat the two-browser test, then restart Postgres and check that the session
and canvas are still there.

Inside the application container, `localhost` names that same container rather
than the Postgres container. We could work around this with host networking,
but Docker Compose gives both containers stable names on the same network.

## Run the stack with Docker Compose

Ask the assistant to describe both services in one file:

```text
Create compose.yaml with two services:

- postgres, using Postgres 16 and a named volume
- app, built from the Dockerfile at the repository root

Configure SDIP_DATABASE_URL so the app connects to the postgres service.
Add a Postgres health check and wait for it before starting the app.
Expose the app on port 8000.

Keep passwords and SDIP_JWT_SECRET in environment variables. Add .env.example,
but don't commit the real .env file.
```

We use the service name `postgres` as the database hostname:

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: sdip
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: sdip
    volumes:
      - interview_canvas_pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U sdip -d sdip"]
      interval: 5s
      timeout: 5s
      retries: 5

  app:
    build: .
    environment:
      SDIP_DATABASE_URL: postgresql+psycopg://sdip:${POSTGRES_PASSWORD}@postgres:5432/sdip
      SDIP_JWT_SECRET: ${SDIP_JWT_SECRET}
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  interview_canvas_pgdata:
```

Inside the Compose network, the application reaches the database at the
hostname `postgres`. The health check also stops the application from starting
before Postgres accepts connections.

Create your local `.env` from `.env.example`, set both secrets, and start the
stack:

```bash
docker compose up --build
```

Check the health endpoint from another terminal:

```bash
curl --fail http://localhost:8000/health
```

Then repeat the interview flow at [localhost:8000](http://localhost:8000). Stop
the stack with `docker compose down`, start it again, and confirm that the named
Postgres volume preserved the data.

## Integration tests

The backend already has tests for authentication, sessions, persistence, and
WebSocket messages. They run through FastAPI's test client against SQLite.
However, they don't prove that the compiled frontend and container work with
Postgres. They also don't test browser cookies and WebSocket connections across
the running stack.

We add a second test suite for the containerized stack:

```text
Add integration tests that run against the application started by compose.yaml.

Use only the public HTTP and WebSocket interfaces. Don't import backend code or
mock the database, API client, or WebSocket connection.

Test this flow:
1. Log in as the seeded interviewer.
2. Create an interview session and a candidate join link.
3. Join from a separate client with its own cookie jar.
4. Connect both clients to the session WebSocket.
5. Change the canvas as the candidate and verify the interviewer receives it.
6. Read the canvas through the API and verify the change was persisted.

Give each test isolated data and clean it up. Add a Makefile target named
integration-test and document how to run it against Docker Compose.
```

Run the complete stack in the background and start the suite:

```bash
docker compose up -d --build
make integration-test
docker compose down
```

Test the green result by changing one important behavior on purpose. For
example, stop broadcasting `document_update` messages or disable
the database write. The integration test must fail. Revert the change and run
the suite again.

The frontend currently has lint and build commands but no separate unit-test
suite. That's fine for this stage because the integration test exercises the
main browser-to-backend flow. Add focused frontend tests when client-side logic
grows beyond what the integration suite can cover clearly.

## Deploy to AWS

You can take the Dockerfile to Render, Railway, Fly.io, or another managed
container host. That's usually the quickest way to get a proof of concept
online.

The current frontend logs in with a seeded development account. Treat this
deployment as a workshop proof of concept, and don't put sensitive interview
data in it. Before real users arrive, remove the development credentials and
add a proper registration or identity-provider flow.

In the workshop, I eventually used AWS because I wanted the infrastructure in
the repository. We deploy the application container to one EC2 instance and use
Aurora PostgreSQL for the database. AWS Secrets Manager stores the database
credentials and JWT secret. CloudFront gives us an HTTPS URL in front of the
instance.

Ask the assistant to create the infrastructure:

```text
Create an AWS CloudFormation deployment for this application.

- Use Aurora PostgreSQL Serverless v2 for the database.
- Store the database credentials and SDIP_JWT_SECRET in Secrets Manager.
- Run the application container on one EC2 instance.
- Put CloudFront in front of the instance and return a public HTTPS URL.
- Configure CloudFront to forward the headers required for WebSockets.
- Don't cache API or WebSocket requests.
- Use /health for the application health check.
- Send application and deployment logs to CloudWatch.
- Create a GitHub Actions OIDC role restricted to this repository and main.
- Make repeated deployments idempotent. Don't rotate secrets on every deploy.

Put the template in infra/cloudformation.yaml. Add scripts/aws-deploy.sh and
document the required AWS CLI setup. Output AppUrl and GitHubDeployRoleArn.
```

CloudFront supports WebSockets, but the distribution must forward the relevant
headers to the origin. The [AWS WebSocket documentation](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-working-with.websockets.html)
lists the headers and origin-request settings.

Before you run the script, authenticate the AWS CLI with an identity that can
deploy the stack. Keep credentials outside the repository. Use a temporary
identity for the initial setup, then remove its access when GitHub Actions can
deploy through OIDC.

Run the generated helper from the repository root:

```bash
./scripts/aws-deploy.sh
```

CloudFormation needs a few minutes to create the database and instance. When it
finishes, the script prints the `AppUrl` stack output.

A successful CloudFormation run only tells us that AWS created the resources.
Open the URL and test the application again with two browser sessions. Create
an interview, join it as a candidate, change the canvas, and confirm that the
interviewer receives the WebSocket update. Also check `/health` and the
CloudWatch logs.

For this article, we keep the application's current startup table creation.
FastAPI can create tables in a new proof-of-concept database, but it can't
safely change an existing schema. Database migrations remain follow-up work
before the schema starts changing.

## CI/CD with GitHub Actions

We ran the deployment script ourselves to get the first version online. Now we
want every change to run the same checks, and we want deployment to happen only
after those checks pass.

Ask the assistant for the workflow:

```text
Create .github/workflows/ci-cd.yml.

Run these jobs in order:
1. Run backend tests and frontend lint/build in parallel.
2. Build and start the Docker Compose stack, then run integration tests.
3. On main only, deploy to AWS through the GitHub OIDC role.
4. Run a smoke test against /health after deployment.

The deploy job must depend on every test job. Use OIDC and short-lived AWS
credentials. Don't store AWS access keys in GitHub.
```

GitHub needs `id-token: write` permission to request an OIDC token. The AWS role
trust policy should restrict the token to this repository and the `main`
branch. AWS recommends this restriction because a broad trust policy could let
another repository assume the role. See the [AWS OIDC guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html)
and [GitHub's OIDC documentation](https://docs.github.com/en/actions/concepts/security/openid-connect)
for the current setup.

Add the `GitHubDeployRoleArn` stack output as `AWS_ROLE_TO_ASSUME` in the GitHub
repository settings. Add the region and any other non-secret deployment values
there too.

Commit and push the workflow:

```bash
git add .github/workflows/ci-cd.yml
git commit -m "Add CI/CD pipeline"
git push
```

On a pull request, GitHub Actions runs the checks and skips deployment. On a
push to `main`, it runs the same checks and deploys only when all of them pass.
The smoke test then calls `/health` on the public URL.

CI/CD only runs the test suite consistently, so it can't make weak tests
trustworthy. Keep the container-level integration test focused on the real
interview flow, and break it deliberately whenever you aren't sure what it
proves.

## Delete the AWS resources

The AWS database and instance cost money while they run. When you finish the
exercise, delete the CloudFormation stack.

Export any data you want to keep before you run this command:

```bash
aws cloudformation delete-stack --stack-name interview-canvas
```

Wait for the stack deletion to finish, then check the AWS console for the EC2
instance, Aurora cluster, and Secrets Manager entries. Remove the temporary
deployment identity or access key if you created one for the first deployment.

## The deployed application

We began Article 2 with a local React and FastAPI application backed by SQLite,
and we now have:

- one container that serves the frontend, API, and WebSocket endpoint
- Postgres for persistent data
- Docker Compose for the local application and database
- integration tests against the running stack
- AWS infrastructure described with CloudFormation
- a GitHub Actions workflow that tests every change and deploys `main`

We still gave the coding assistant separate, bounded tasks. At every stage, we
ran what it produced and checked the behavior that mattered. The commands can
succeed even when the application doesn't work. Both browser sessions must
be able to use the interview canvas together before we call the deployment
ready.

In the next article, we'll move from deployment to DevOps and observability.
We'll cover logs, metrics, and alerts, then see how coding agents help us
respond to failures and operate the application.
