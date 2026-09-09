# Homework 3: Test, Containerize, and Deploy an AI-Assisted App [DRAFT]

In this homework, we take the app you built in Homework 2 the rest of the way: proven by tests that exercise the real stack, packaged in containers, checked automatically on every pull request, and deployed so other people can use it.

The path:

```text
integration tests
containerization
continuous integration
deployment
continuous delivery
```

A generated `Dockerfile` that builds is not the same as one that builds the right thing, and a green pipeline that skips the tests is worse than no pipeline. So the workflow stays the same: let the agent produce the first version, then read it, run it, and break it on purpose to see whether it actually catches anything.

Keep using the coding agent from the previous homework. You will also need Docker installed, and an account on a deployment service like Render, Fly.io, Railway, or Cloud Run.

## Homework Idea

Continue with the app from Homework 2 and apply each step of the path to it. At the end, the app should be deployed at a public URL, rebuilt and redeployed automatically when you merge to the main branch, and reproducible locally from the README.

## Question 1: Integration tests

Unit tests check pieces in isolation. Now let's prove the whole stack works: API endpoints against a real database, migrations included — and fast enough to run on every push.

Ask your agent to write integration tests that hit a real database and cover the frontend-to-backend flow.

What do integration tests check that unit tests don't?

- How components work together, e.g. the API against a real database
- The output of a single function in isolation
- How the UI looks on the screen
- How fast the application is

For this and next questions you can ask your coding assistant to select the correct option.

## Question 2: Dockerfile

Let's containerize the app. Ask your agent to create a multi-stage Dockerfile that builds the frontend and serves it together with the backend in one image.

Which command builds an image from a Dockerfile?

- `docker build -t app .`
- `docker run build app`
- `docker compose up build`
- `docker init`

## Question 3: Multi-stage builds

Your agent probably used a multi-stage build. Why?

- The final image stays small, because the build tools never ship in it
- One container can run two operating systems
- It makes the tests run faster
- Docker Hub requires it

## Question 4: Docker Compose and Postgres

It works with SQLite, but how about Postgres? Ask your agent to add a `docker-compose.yml` with the app and Postgres, and switch the backend to Postgres there. Then run it:

```bash
docker compose up --build
```

Which file describes how the containers run together?

- `docker-compose.yml`
- `Dockerfile`
- `openapi.yaml`
- `deploy.yml`

## Question 5: Continuous integration

Now let's check the app automatically on every pull request. Ask your agent to set up GitHub Actions CI that runs linting, unit tests, integration tests, and the container build.

In which directory do GitHub Actions workflow files live?

- `.github/workflows/`
- `.github/`
- `workflows/`
- `actions/`

## Question 6: Deployment

Now let's deploy it. Ask your agent:

```text
I want to deploy this app so other people can use it.
What are the options? Pick one together with me and walk me
through the deployment. Run database migrations on deploy.
```

Which service did you use for deployment?

## Question 7: Continuous delivery

Wire up CI/CD so that merging to main automatically builds, migrates, and redeploys the app.

What gates the automatic redeploy?

- The CI checks (tests) pass on the merge to main
- Nothing, it deploys every push
- The model's confidence that the code is correct
- A manual upload to the server

## Question 8: Smoke test

A deploy that "succeeded" is not the same as an app that works. Ask your agent to add a post-deploy smoke test that hits the public URL after each deploy.

What does a post-deploy smoke test do?

- Checks that the deployed app actually works at its public URL
- Measures CPU usage on your laptop
- Tests the app locally before the deploy
- Deletes the database before deploying a new version

## Submission

Submit your homework here: https://courses.datatalks.club/ai-dev-tools-2026/homework/hw3

Put the public URL of your deployed app in the `README.md`. Use the link to your repository in the homework submission form.

Don't forget to commit your code at every step. And when you no longer need them, stop or delete the resources on the deployment service — most of them are chargeable.

## Learning in Public

We encourage everyone to share what they learned. This is called "learning in public". Read more about why it matters here: https://aishippingblog.com/p/benefits-of-learning-in-public

Learning in public is one of the most effective ways to accelerate your growth. Here's why:

1. Accountability: Sharing your progress creates commitment and motivation to continue
2. Feedback: The community can provide valuable suggestions and corrections
3. Networking: You'll connect with like-minded people and potential collaborators
4. Documentation: Your posts become a learning journal you can reference later
5. Opportunities: Employers and clients often discover talent through public learning

Don't worry about being perfect. Everyone starts somewhere, and people love following genuine learning journeys!

### Example post for LinkedIn:

```
🚀 Week 3 of AI Dev Tools Zoomcamp by @DataTalksClub complete!

Took the app I built with AI from "works on my machine" to a public URL!

Today I learned how to:

✅ Write integration tests that hit a real database
✅ Package the app with a multi-stage Dockerfile and Docker Compose
✅ Swap SQLite for Postgres
✅ Set up GitHub Actions CI on every pull request
✅ Deploy — and redeploy automatically when tests pass

Here's my repo: <LINK>
Live app: <URL>

Following along with this amazing course - who else is shipping with AI?

You can sign up here: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/
```

### Example post for Twitter/X:

```
🚀 Deployed my AI-built app to a public URL!

✅ Integration tests on a real database
🐳 Multi-stage Dockerfile + Compose
⚙️ CI on every PR
🔁 Auto-deploy on merge to main

My repo: <LINK>
Live app: <URL>

"Works on my machine" is no longer the goal.

Join me: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/
```
