# From Zero to Production with AI Coding Agents

[AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp)
is the free course we run at DataTalks.Club. 

Across the series we build an application with AI coding agents from the idea to making it production-ready.

I showed how to do it in 3 stages:

- [Stage 1: Build](https://aishippingblog.com/p/build-and-ship-a-full-stack-app-with) - coming up with an idea, creating frontend and backend and running it locally
- [Stage 2: Deploy](https://aishippingblog.com/p/deploy-a-full-stack-app-with-ai-coding) - making the application testable, deployable and setting up CI/CD 
- [Stage 3: Operate](https://aishippingblog.com/p/devops-and-observability-for-an-ai) - adding dev/prod environments, collectings metrics, logs, and traces and having AI agents react to incidents 

In this article I'll put everything together in one place, so you can use it as a reference for developing your projects. I will not go into the details of each step, but I'll give you the prompts that you can use to build a production-ready project end-to-end just by following this article. 

In the previous articles, I tried to keep it tool-agnostic, but I used FastAPI, AWS, CloudFormation and other technologies in the prompts. Here, I don't assume any programming language, framework, database, cloud, or observability tool. Instead, I'll show you how to use AI to make these decisions. 

Each step here is a prompt that you put into your coding assitant. You can choose any assistant, it doesn't matter. In most cases, it helps to start a new session for each step. Then only the important things are in your agent's context and it can finish the work faster and better. 


## Build

In the build stage, we:

- turn the raw idea into a specification
- create frontend
- create backend
- connect them


### 1. Specification

If you give a coding agent a vague idea, it'll fill in the gaps with its own assumptions, and you'll get an app you didn't wan.t 

It's better to be very clear what you want and capture this in a document called "speficiation". 

I usually use ChatGPT for that: I open it in dictation mode and do a brain dump with my idea, and then we iterate until it's clear how it can look like.

You can start you dicussion with your AI assistant using this prompt:

```text
I want to build a tool for forming study groups.

Help me set the scope for this project precisely. I want to brainstorm with you and understand how the tool should work. Give me options.

Ask me one question at a time and keep your output short.
```

At the end, ask the assistant to summarize the discussion into a markdown document. 

Create an empty folder for your project, and save the specs into `_docs/specs.md`

Use this document to build the frontend.

### 2. Frontend first, mocked

I build frontend before backend so I can test the idea quickly. It's the least expensive way: you create a clickable interface and you test it with some mock data. If it looks the way you want, you can continue.

Put this into your coding assistant (or tools like Lovable, v0 or Bolt.new):

```text
Create a system design interview application.

[Paste the ChatGPT-generated specification here.]

Centralize every backend call in one services layer, and create a mock implementation of it so the whole app runs without a real backend.

Add tests.
```

Save the frontend code in the `frontend/` directory. 

After you iterated on frontend and you like it, time to define how it will interact with backend.

### 3. Manual test

Come up with a test that you can use for validating that your application works. This should be a sequence of actions that you perfmorn to validate that the app works the way you want

For an app that helps you find study partners, it could be something like

1. Open the home page, sign up
2. Create a group for styding
3. Create an event there
4. Share the event
5. Sign up to the event from another browser session
6. Verify that the sign up is visible in the first session  

You can use AI to compe up with this scenario, but remember it - and maybe save it to `_docs` too.


### 3. AGENTS.md

AGENTS.md is loaded into the agent's context every time you start a new session. You can add anything that you think is important for your app. For now let's add one line there:

```
make focused regular commit and explain your decisions in the commit messages so we can use it as logs
```

TODO: update the numers 


### 3. OpenAPI schema

Our frontend uses mock data, but it works the way we want. We previously asked the assistnat to centralize all the future backend calls in one place. Now let's use this to create the API specification. We will use this specification to define frontend-backend interaction:

```text
Read the frontend's API client in frontend/

Create openapi.yaml at the repository root that defines every endpoint, method, path, request body, response body, and which endpoints need authentication.
```

Now we have the speficiation for our backend so we can build it.

### 4. Choose the backend stack

Before we actually build it, you need to decide which technology you want to use for this application. 

Ask the coding assistant to help:

```text
Based on openapi.yaml, propose 2-3 backend stacks options. Describe pros and cons for each. Recommend one.
```

You can challenge your AI assistnat and ask it some questions, or just accept the option it suggests. 

At the end, save the results to `_docs/stack.md`

### 5. Backend

We have selected the technology so let's use it to build the backend.

Just like we created frontend with a mocked backend calls, we can create backend with a mocked database. You first focus on making sure the frontend-backend integration works, and then you can connect a proper database.


```text
Build backend in backend/ based on `_docs/stack.md` that implements the openapi.yaml spec.

Use an in-memory store and seed it with data so the frontend has something to show.

Add authentication with hashed passwords and bearer tokens for the endpoints that need it.

Write tests
```

### 6. Makefile

I always have problems remembering how to start the backend, how to run the frontent, install the dependendencyes and do other things. For that I usualy use makefiles, so I can just type

```
make backend
```

And the backend runs. Let's define a Makefile for us:


```text
Create a Makefile so I can easily run the applicaiton
```



### 7. Connect frontend and backend

We created a backend but the frontend still serves the mock data. Let's connect them:

```text
Switch the frontend to use the real backend client.
```

Use the test scenario from before to make sure it works. 

You may do a few iterations here. Test the application and ask the agent to fix the problems you dicosver until it works correctly. 


### 8. Database

We don't have a real database yet. let's add it. I usually use SQLite for local development, so I'll use it here, but feel free to replace it with something else.

```text
Replace the in-memory store with a database. Use SQLite with ORM, so later we can easily switch to a different database. 
```

Instead of SQLite your application may need something else, so you can chat with your coding assistatnt about it before you implement it. 

After it's done, use the test scenario it and iterate until it fully works.


## Deploy

Our app works locally. Great. Let's deploy it - make it available for others to use:

- Containerize it
- Deploy it to the cloud 
- Automate the deployment with CI/CD

### 9. Containerization 

We need to put our application in a container, so we can later use any container management system for deployint it. 

In our local environment, we have two processes: one for frontend, one for backend. We need to run them separately. In practice, you usually compile frontned into static files and serve them with backend. 

So, instead of creating separate containers for fronent and backend, we'll create one that serves both:

```text
Create a Dockerfile that builds the frontend with Node, then builds backend.
Backend should serve the frontend.
```

Build and run the image, then verify the flow with the test scenario and iterate until it works. 

### 10. Production database

In the previous stage (build) I used SQLite. It helps with keeping the local setup lightweight, but it's not a database we can use in production. Typically we use something like Postgres. 

You can ask your agent to select the best database for your case, but it's very likely it'll be Postres. 

So let's add it:

```text
Add Postgres support to the backend.
```

Use the test scenario to make sure the app works.


### 11. Docker Compose

To make it easier to manage the dev environment with all the services locally we use docker compose. 

Let's ask the agent to define it:

```text
Create docker-compose.yaml with two services: database and the app.
```

Run it with `docker compose up` and test it.


### 12. Integration

It's possible that by now you already have tests. AI coding assistants are instructed to create them. But maybe in your project there are still none. 

Let's make it explicit and ask the asistant to create thme

We also want to have a specific category of tests - integration tests. These tests are used to make sure the interaction between backend and the database is correct.  

You can also ask the asisstnat to help you with findign the right test scenarios to include in the test suite:

```text
Create integration tests that run against docker-compose.yaml.
What scenarios should we test?
```


### 13. End-to-end test

Integration tests verify that the backend can connect to the datbase. End-to-end tests verify the entire user-backend flow: from the browser to the frontend, from the gfrontend to backend, and from the backedn to the database. 

So far we were doing these tests oursevles manually. Let's now automate it.

```text
Add an end-to-end test that runs against docker-compose.yaml.

Use Playwright to:

1. <Describe the first step>
2. <Describe the second step>
3. ...

Put the tests in the e2e/ folder in the repository root.
```

Now we don't need to repeast this test manually every time we make a change. 



### 14. Deployment stack

Now the application works locally and properly tested. It's time to deploy it. But where? There are many options. Let's choose what works best for us.

Ask the coding agent: 

```text
Propose 2-3 ways to deploy the application. Compare cost, complexity and other factors.

<List any other contraints that you have>
```

It's also helpful to use an infrastructure as code (IaC) tool to manage your cloud resources. 

```
I want to use an infrastructure-as-code tool for managing my infra. What are my options?
```

It's possible that for the deployment option you chose there are no infrastructure-as-code options. In this case, just move on.

### 15. Deployment

Now we selected the stack, so let's deploy. 

Ask the agent:

```text
Deploy this application to <Selected option>.
```

If applicable, add

```
use <IaC tool> for managing the infrastructure
```


### 16. CI/CD pipeline

We can deploy a few times manually, but we want to automate it. It's done with CI/CD:

- CI is continuous integration - running tests every time you push to git
- CD is continuous deployment - automatically deploying when the tests pass

```text
Create a CI/CD pipeline that:

- runs backend and frontend tests in parallel
- builds the Docker Compose stack and runs integration and end-to-end tests against it
- deploys the application
- validates that the deploy is successful by checking the health endpoint
```

You probably use GitHub for hosting code, so it's likely that you'll use GitHub Actions. If you don't like it, chat with AI to select a different option.

We successfully deployed our application, but we're not done yet. We need to make it more production-ready.

## Operate

To make it more production-ready, we need to add a few things:

- create dev/prod environments
- capture metrics, logs, and traces
- set up alerts 
- have an AI agent taking care of the alerts 

Let's do that

### 17. Second environment

Now each push brings the updates directly to the deployment. But what if it has a bug that we missed? 

To avoid that, we have two environments:

- Dev: environment for testing. We deploy here on every push
- Prod: envrionent that real users use. We promote a release from dev to prod only when we confirm that it works correctly

If we use infrastructure as code, it's trivial to set up. If not, let the agent handle it.

Ask:

```text
Create a second, independent copy of our infrastructure. We will use the copy as production, and the existing infrastructure as a dev environment.
```

### 18. Manual promotion workflow

Now we automatically release the code to development on every push. Let's set manual release pormotiion from dev to prod:


```text
Create a manual GitHub Actions workflow that promotes the dev version to production.
```

### 19. Split build/deploy

It's possible that in your CI/CD the build and deploy happens in one step (it happened to me when I was deploying to AWS EC2). 

It's an anti-pattern. We want to build the image only once, and first deploy it to development, and if it works fine, we use it for production too.

If for you these steps are not separate (you can ask AI if you're not sure), let's split them. 

Ask:

```text
Currently we build the image during the deploy stage.

Split it into two stages:

- Build: build the image and push it to a container registry
- Deploy: pull the image from the registry and serve it

The manual prod promotion CI/CD workflow pulls the currently deployed dev image to prod.

Tag each image using the YYYYMMDD-HHMMSS-shortsha pattern (e.g. "20260818-163457-83242da")
```

Depending on where you deploy your application, you may have to use different options for the container registry. talk to AI if you're not sure what to select and how to do it.

### 20. Observability. Instrument with OpenTelemetry

Our application is deployed and serving real users in production. But we don't know how reliable it is.

We need data for that. that's called telemetry and we will colllect metrics, logs and traces. The intrustru standard is OpenTelementy so you'll probably use it. 

```text
Instrument the backend with OpenTelemetry.

Include in the telemetry:

- service name
- environment
- deployed version
```

To "instrument" backend means to include the code for capturing the telemetry in our application. But we also need to save it somehwere.


### 21. Choose the observability backend

There are many options for storing the telemetry and displaying the dashbords. Some are open-source but you need to self-host it. Some are fully managed, but you'll need to pay for them. Some of the self-hosted options give a generous free tier. 

Ask the agent to help us select:

```text
Propose 2-3 options for storing the telemetry (metrics, logs, traces) via OTel and for displaying them on a dashboard.

<If you have any preferences add them here>
```


### 22. OTel Collector stack

How we've selected the stack. If you decided to go with open-source and self-hosting, you can also deploy it locally:

```text
Add an OpenTelemetry Collector.

Create "observability/" directory with Docker Compose for: <list selected technologies>

Keep this as a separate Compose project from the application stack.
```

Then deploy it:

```text
Deploy the observability stack. It should be separate from the application stack.
Connect both development and production to it.
```


If you decided to go with a managed service, connect it:

```
Add an OpenTelemetry Collector for <selected technology>. Help me configure it
```



### 23. Application metrics

We configured OTel. Let's collect important metrics. 

They are application-dependent and depends on what's importnat for your product. 

You can also ask the agent to come up with the most important metrics:

```
What are the most important product metrics I need to track in my application? Give me top 5
```

Start tracking them: 

```
Track the following metrics with OTel

- <List them>
```



### 24. Dashboards

We're tracking the metrics but not displaying them yet.

Let's fix that:

```text
Display the metrics we export in a dashboard.
Make it possible to filter by environment and deployed version
```



### 26. Alert

We can't babysit the metrics in a dasbboard. Instead, we can configure an alert that will fire every time the metrics goes too low or too high. 

```text
Add an actionable alert for <most important metric> 
Include the service, environment, deployed version, owner, and dashboard URL in the alert.
```

It's also useful to track 5xx error codes and for each error send an alert (or configure a threshold that makes sense for your application). Talk to your AI assistant to set it up.


### 27. On-call worker

Now alerts land in our email or slack. But we still need to act on them.

We can have AI watch the alerts and fix the errors when they happen. 

Let's configure it

```text
Add an on-call-engineer/ directory with a script that connects to the observability alerts API.

When an alert fires, wake up an on-call agent that you run in jeadless mode, pass all the alert details. The on-call agent should be able to resolve the issue autonomously and commit the fix.
```

The agent should:

- investigate first
- reproduce the failure
- only patch if the fix is small, tested, and committed to an isolated branch

You give the on-call engineer these instructions:

```
You are the on-call engineer for this repository. An alert just fired.

Investigate the root cause. Read the code and reproduce the failure.
If you find a real bug, make the smallest correction, run the backend tests,
and commit the fix with a clear message.
If the alert is a false positive, explain why and do not change the code.
```

## Going Further

This setup brings our application closer to production. But there are still many things you need to think about:

- Do you use a container manager? if not, consider using it
- Do you use a managed database service? If not, consider usint it.
- Regularly back up your database and test that the backups actually work.
- Learn about VPCs and see if you need one. 
- When you start getting traffic, learn about scaling and load balancing. 

Also, periodically ask Fable or GPT-5.6-Sol Max (better both) to audit your code for security vulnerabilities.

I'm only sctaching the surface of a "real production system" in this article, but the stages and steps in this tutorial are more than enough to get started. 

With this setup, you can use AI to build a product that runs reliably. The rest you can learn when you actually need it. 

Have fun building! And check our AI Dev Tools Zoomcamp if you want to learn more about using AI for increasing your development productivity. 