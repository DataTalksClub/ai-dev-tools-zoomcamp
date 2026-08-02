# Visual plan for the end-to-end article

Use diagrams when the reader needs to understand a sequence, dependency, or
architecture. Use screenshots when the visual proof matters more than the
structure. Keep each visual focused on the point of its section instead of
repeating the full overview.

| Article location | Format | Visual direction | What it should explain |
| --- | --- | --- | --- |
| Introduction | Product screenshot | Show Snake Royale in play, with the leaderboard or spectator view visible beside the game. | Give readers an immediate picture of the app they will build. |
| Overview | Workflow diagram | Use the completed three-row overview: frontend, API contract, backend, connection, persistence, containers, AWS, CI/CD, public app. | Show why the order matters and how each stage creates the input for the next one. |
| Frontend first | Annotated screenshot | Show the running frontend with two small callouts: “mock backend” and “central services layer”. A second small code-tree inset can show `mock.ts`, `http.ts`, and `index.ts`. | Prove that the UI works before the backend exists and make the service switch concrete. |
| Give the assistant the house rules | Editorial illustration | Show `AGENTS.md` at the repo root next to a coding-agent terminal using `uv` and committing changes. This should look like a file-and-terminal composition, not a flowchart. | Show that one small file controls the agent's recurring project conventions. |
| The spec between the two sides | Contract diagram | Put `openapi.yaml` in the center, with the React services layer on the left and FastAPI routes on the right. Arrows from both sides should point to the contract. | Show that the frontend and backend agree through one explicit document. |
| The backend from the spec | Comparison screenshot | Place the relevant part of `openapi.yaml` beside FastAPI's `/docs` page for the same endpoint. Highlight the matching path, method, request, and response. | Show how the written contract maps to the routes the backend actually exposes. |
| Connecting them | Request sequence diagram | Browser → React component → HTTP services client → FastAPI route → response. Add one red mismatch branch returning `422`, then a correction against `openapi.yaml`. | Show the normal request path and where integration debugging happens. |
| Persistence | Evolution diagram | Show the same repository or store interface connected first to memory, then SQLite, then Postgres. Keep `DATABASE_URL` fixed above the three implementations. | Show that the interface stays stable while the storage implementation changes. |
| Containers | Build-and-runtime diagram | On the left, show the Node build producing static files and those files entering the Python image. On the right, show Docker Compose running the app beside Postgres and a named volume. | Explain both the multi-stage image and the runtime topology without mixing them into prose. |
| Deploying it | AWS architecture diagram | Browser → public EC2 instance running the app container → Aurora PostgreSQL. Connect EC2 to Secrets Manager, and draw one CloudFormation boundary around the AWS resources. | Show what gets deployed and which service owns data and credentials. |
| The pipeline, and taking the keys away | CI/CD diagram | Start with a push to `main`; split into frontend and backend tests; merge into integration tests; continue to deploy. Add GitHub OIDC → AWS as a short-lived authentication path. | Show the test dependency graph and why no long-lived AWS key is needed. |
| What we left out | Maturity roadmap | Use a simple staircase or horizon: CORS, persistent sessions, migrations, managed hosting, WebSockets. Avoid implying that every app needs every step immediately. | Show when the shortcuts in the first version begin to matter. |
| What changes after the first version | Before-and-after diagram | Left: one person gives one prompt at a time. Right: specification → backlog → implementation → independent verification → pipeline. | Show the shift from exploratory prompting to a repeatable development workflow. |
| Next in the series | Series roadmap illustration | Use three connected cards for agent capabilities, security and DevOps, and the reader's own end-to-end project. | Preview the remaining modules without introducing another technical architecture. |

## Recommended production order

1. Keep the overview diagram already added to the article.
2. Create the API-contract, container, AWS, and CI/CD diagrams next. They carry
   the most explanatory value.
3. Capture the product, FastAPI docs, and frontend-service screenshots from the
   working Snake Royale repository.
4. Add the maturity roadmap and before-and-after workflow only if the article
   still needs more visual breaks.
5. Treat the `AGENTS.md` and series-roadmap visuals as optional polish.
