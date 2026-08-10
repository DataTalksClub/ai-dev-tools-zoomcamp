# Deploy a Full-Stack App with AI Coding Assistants

This is the third article in a series for [AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp),
the free course we run at DataTalks.Club.

In this article, I want to take a web application and make it accessible for everyone on the internet. 

We will:

- Take the application that's already working locally
- Containerize the application 
- Switch from SQLite to Postgres
- Add integration tests
- Deploy to AWS
- Set up CI/CD via GitHub Actions


It's based on the second half of the full-day workshop I did for AI Shipping Labs:
[Build and Deploy a Full-Stack App with AI Coding Assistants](https://aishippinglabs.com/workshops/full-stack-vibe-coding).


## Recap

In the [previous article](https://alexeyondata.substack.com/p/build-and-ship-a-full-stack-app-with),
we started building an application for system-design interviews. An interviewer creates session and shares a link with a candidate. When the candidate updates something on the canvas, the interviewer sees the updates in real-time.

- First, we created the frontend only with React
- Then we created OpenAPI specification for defining the frontend-backend contract
- Next, we created the backend from this contract
- We added database support with SQLite and SQLAlchemy

You can find the code in the
[interview-canvas-share](https://github.com/alexeygrigorev/interview-canvas-share)
repository.


## Containerization

When we run the application locally, we need to execute two commands: one for frontend and one for backend:

```bash
# TODO run vite
# TODO run uvicorn
```

And they run in two separate processes. This is okay for development, but not convenient for production.

In practice, we usually build the frontend and get a bunch of html, css and js files. These are static files (they don't change as long as we don't change the code). We can take these files and serve them with backend. 
This way, we only need to deal with one container that serves both frontend and backend, not two separate ones.  

Ask the coding assistant to create it:

```text
Create a Dockerfile that builds the frontend with Node, then builds a Python image with backend with frontend static files. Backend should serve the frontend.
```

As the result, we see a two-staged Docker build: 

- First, we have a nodejs-based image, we use it for compiling the frontend
- Then in the second image, we build backend, and also copy the frontend from the first step (without all its nodejs dependencies)

Here's the fininished [Dockerfile](https://github.com/alexeygrigorev/interview-canvas-share/blob/main/Dockerfile).

Then we build and run the image. 

In my case, I can see the result at [localhost:8000](http://localhost:8000).

Let's test it:

- Create an interview session
- Open the join link in a different browser window
- Move an element in the candidate window
- Check that the interviewer sees the change


## Switch from SQLite to Postgres

SQLite is very convenient: all the data is in a single file, and it runs fast locally. 

But it's not suitable for production. For production, we typically use Postgres or similar databases. 

When we set up the foundation in the previous article, we asked the coding agent to use SQLAlchemy. Because of that, our application can easily switch between different database engines. 

Let's start Postgres locally:

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

Now ask the assistant to use it:

```text
Add Postgres support to the backend.
```

Once it finishes, repeat the two-browser test.

## Docker Compose

Running two docker sessions is not convenient. Let's create a common Docker Compose file that we can use for local development.

Ask the assistant to implement it:

```text
Create docker-compose.yaml with two services: postgres and the app
```

## Integration and end-to-end tests

The agent might have created some tests. If it doesn't, we can ask it to create it:

```
Create integration test that verify that frontend and backend work end-to-end.
What scenario we should test?
```

Now let's add another one. We added two things that can break, so let's test them too. 

We will verify that:

- Frontend compilation works correctly
- The backend can communicate with Postgres

Let's ask the agent to implement a test:

```text
Add an end-to-end test that run against docker-compose.yaml

Use playwright to:

1. Log in as the interviewer (session 1).
2. Create an interview session
3. Share the join link
4. Join from a separate client as the candidate (session 2)
4. Change the canvas as the candidate (session 2)
5. Verify that the interviewer sees the change (sessoin 1)
```

## Deploy to AWS

We're now certain that the application works well. So we can deploy it. 

We have a lot of options. Our application is nicely containerized and only needs Postgres for running. We can deploy it to Render, Railway, Fly.io, or another managed container system. 

Last year, we deployed to Render. This year, I want to deploy to AWS. You don't have to do it with AWS and ask the coding assistant to recommend the best environment. 

Let's do the deployment:

```text
Deploy this application to AWS. Use AWS CloudFormation
```

When I do it for the first time, I use a user with the Admin permissions. But after the agent figures the setup out, I take these permissions away. The further deployment will happend only via CI/CD.  

## CI/CD with GitHub Actions

Every time I make a change, I want the changes to apply automatically. For that, we use CI/CD via GitHub Actions. 

Every time we make a push to main, we want to:

- run frontend and backend tests
- build the containers 
- run the integration tests
- run the end-to-end tests
- if all the tests pass, deploy the new version

For the last step, the computer with GitHub actions needs access to our AWS account. We can't give the admin access permissions there - it's too dangerous. We need to give it the minimal set of permissions that are only enough to do the deployment and nothing else.

This is done with OIDC (OpenID Connect). The GitHub actions runner gets assigned a role from AWS and can access all the resources it needs.

Let's create the role and the workflow:


```text
Create a CI/CD pipeline that:

- runs backend and frontend tests in parallel
- build the docker compose stack and runs integration and e2e tests against it
- deploys to AWS using an GitHub OIDC role
- validates that the deploy is successful by checking the health endpoind
```

Now let's change something in our application, commit and push. Wait for a few minutes to see that the change is live.

## Clean up

When we're done, we need to delete all the resources. Because we use the Infrastructure-as-Code approach, we can just delete the CloudFormation stack:

```bash
aws cloudformation delete-stack --stack-name interview-canvas
```

Wait for the stack deletion to finish.

## Application deployed. What's next?

This is what we have done so far:

- We created the frontend application with React
- Then we defined the frontend-backend contract with OpenAPI specs
- Based on the specs, we created the backend
- Next, we added database support with SQLite and SQLAlchemy to the backend
- To make it easier to deploy the application, we put both frontend and backend inside one container. The backend serves the frontend.
- To go to production, we replaced SQLite with Postgres.
- Next, we simplified running everything locally with Docker Compose 
- Once everything was in Compose, we created an end-to-end test
- We took the application that worked locally and deployed it to AWS using CloudFormation
- Finally, we created a CI/CD deployment pipeline, so every time we make a change, this change is automatically deployed.

But there's a lot more we should do to make it possible for the app to run reliably. 

We will cover it in the next lesson:

- Dev and prod environments
- Observability: logs, mertrics, alerts
- Using AI as the first responder when the application stops working
