# DevOps and Observability for an AI-Built App

This is the fourth article in a series based on
[AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp),
the free course we run at DataTalks.Club.

All articles in the series:

- Part 1: [AI-Native Development: Specifications, Loop and Graph Engineering](https://aishippingblog.com/p/ai-native-development-specifications)
- Part 2: [Build and Ship a Full-Stack App with AI Coding Assistants](https://aishippingblog.com/p/build-and-ship-a-full-stack-app-with)
- Part 3: [Deploy a Full-Stack App with AI Coding Assistants](https://aishippingblog.com/p/deploy-a-full-stack-app-with-ai-coding)
- Part 4: [DevOps and Observability for an AI-Built App](https://aishippingblog.com/p/devops-and-observability-for-an-ai) (this article)
- Part 5: TBA

In part 2, we developed an application for conducting system design
interviews. In part 3, we deployed it to a cloud environment and configured
CI/CD.

In this part, we make the deployed application easier to operate:

- Separate development and production environments.
- Promote the exact version tested in development.
- Collect metrics, traces, and logs.
- Alert on a user-visible failure.
- Use an AI agent as the first responder.


<figure>
  <img src="images/04-devops-overview.svg" alt="A user pushes a change through CI/CD to development; a release owner promotes the tested release to production, where telemetry flows through observability and alerting to an AI agent">
  <figcaption>Deploy changes to development first, promote a tested release to production, and respond to observed failures</figcaption>
</figure>

We will continue using AWS and CloudFormation, but the principles we show in this article are tool-agnostic and will work for any environment.


## Recap


We started building the [Interview Canvas project](https://github.com/alexeygrigorev/interview-canvas-share) in [Part 2: Build and Ship a Full-Stack App with AI Coding Assistants](https://aishippingblog.com/p/build-and-ship-a-full-stack-app-with):

- We brainstormed with an AI assistant to come up with the specification
- Based on that we created a React-based frontend with no backend
- Next, we defined the frontend-backend OpenAPI schema
- Using the API contract we created the backend
- We added database support with SQLite and SQLAlchemy


<figure>
  <img src="images/02-backend-sqlite.png" alt="A user interacts with the frontend, which calls the FastAPI backend backed by SQLite">
  <figcaption>TODO update the caption</figcaption>
</figure>


The app was running locally, and then we deployed it in [Part 3: Deploy a Full-Stack App with AI Coding Assistants](https://aishippingblog.com/p/deploy-a-full-stack-app-with-ai-coding):

- We containerized the application
- Then added Postgres support
- To make sure the system works reliably, we created integration and end-to-end tests
- We deployed it to AWS
- In the end, we set up CI/CD via GitHub Actions, so every push runs the tests
  and deploys the app to development

<figure>
  <img src="images/04-ci-dev.png" alt="A successful CI/CD run that tests the application and deploys it to development">
  <figcaption>Each tested push is deployed to development. Production promotion is a separate step</figcaption>
</figure>

Now we take the application that's already deployed and make it follow production best practices.


## Dev and prod environments

When we push the code, we automatically deploy this code and the changes to live immediately. It's okay when we only start working on our project. But when we have real users, we want to be more careful, and check if our changes didn't introduce any problems.

To avoid having this problem, we usually have two copies of the same environment:

- Dev (development): the environment we use internally for checking that everything works. Typically we run the latest version of our project there, and every time we push, the changes are automatically deployed there.
- Prod (production): this is what our users use. We don't want to deploy every single change there automatically and we want to have more control over the process.

TODO: figure: take the dev/prod split from images/04-devops-overview.svg and keep only it


Because we previously defined our infrastructure as code, duplicating it is trivial. We most likely will need to change a few things, like the size of the machine where the application is running (production typically needs a more powerful machine), but the majority of the resources will stay the same.

Let's ask our coding assistant to create a copy of the existing environment and call it "production":

```text
Create a second, independent copy of our infrastructure. We will use the copy as production, and the existing infrastructure as a dev environment.
```

Once we have the prod environment, let's update our CI/CD. We will only deploy to dev on every push. For production, we will have a manual action that will take whatever development has and _promote_ (apply) it to production.

```text
Create a manual GitHub Actions workflow that promotes the dev version to production.
```

<figure>
  <img src="images/04-manual-production-deploy.png" alt="A manual production deployment workflow with a confirmation checkbox and an optional release tag">
  <figcaption>A person approves the production deployment and can select the release to promote</figcaption>
</figure>

Now we have two environments.


## Container image repository

In the pipeline we have so far, the Docker image is built during the deploy stage. I deploy to EC2 by executing the build script on the machine and then running the image in Docker.

It's an anti-pattern.

There are multiple problems with this approach:

1. The deploy stage is actually two things: build and deploy. If build fails, there should be no deploy, so it's better to have these steps separately.
2. When we promote the dev version to production, we have to build again. During this time, many things could have changed, so the build will not be identical to dev, and it can cause problems.

So we split the deploy step into two separate steps and then:

- Build the image and upload it to a container registry
- Pull this image from the registry during the deploy
- When promoting to prod, we simply pull the same image to prod

For AWS, we can use [Amazon ECR](https://aws.amazon.com/ecr/) as the container registry. You can also push your images to Docker if you're running outside of AWS and your cloud doesn't have a special service for that.

<figure>
  <img src="images/04-build-once.svg" alt="A user pushes a change, then CI/CD runs separate Build and Deploy steps; the version tag goes to Deploy and a manually triggered Prod release, which updates Production">
  <figcaption>Inside CI/CD, Build and Deploy are separate steps. The version tag goes to development through Deploy and to the manually triggered production release.</figcaption>
</figure>

Let's implement that:

```text
Currently we build the image during the deploy stage.

Split it into two stages:

- Build: build the image and push it to a container registry (ECR)
- Deploy: pull the image from the registry and serve it

The manual prod promotion workflow pulls the currently deployed dev image to prod.

Tag each image using the YYYY-MM-DD-gitsha1 pattern (e.g. "2026-08-18-a1b2c3d")
```

TODO finish


## Observability

Having two environments helps us avoid accidental pushes with buggy code to production. But accidents will still happen, and we need to make sure we detect them and can react in time as fast as we can.

For that we need to have observability. "Observability" means collecting information about the application so we can
understand its behavior and investigate problems.

We achieve observability by adding monitoring to our applications. At the minimum, we collect basic performance metrics like CPU and memory utilization and requests per second (RPS).

If we see that CPU and memory utilization are growing and RPS is dropping, something is definitely off and we need to investigate.

TODO explain more about it so it links clearly to OTel (becaues we don't need otel for cpu and memory)


## OpenTelemetry

To collect this information, we'll use [OpenTelemetry](https://opentelemetry.io/docs/) (often abbreviated as OTel).

The OTel specification defines how applications produce and export telemetry. TODO: what exactly "telemetry" is?
OTLP is the protocol applications use to send telemetry to a collector or backend.TODO is OTLP relevant here?

For many popular libraries, we can add telemetry with just a few lines of code. This process is called "instrumenting" - injecting extra logic for collecting telemetry into existing libraries (like FastAPI) without changing their code.

Let's do it:

```text
Instrument the backend with OpenTelemetry.

Include:

- service name
- environment
- deployed Git commit

in the telemetry.
```

OTel (OTLP) only describes what data we collect, but we don't specify how or where.  Let's do it now. (TODO check it - is it correct to say that?)

## OTel Collectors

We capture telemetry with OTLP, but it doesn't go anywhere. Next, we need to define where exactly we send it. For that, we define
an [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)
between the application and the storage systems.

<figure>
  <img src="images/04-observability-pipeline.svg" alt="An application sends metrics, logs, and traces through an OpenTelemetry Collector into telemetry storage; dashboards support investigation while alert rules independently detect user impact">
  <figcaption>The collector sends signals to telemetry storage; dashboards support investigation, while alert rules detect user impact</figcaption>
</figure>

There are many places where you can send this data to. You can talk to your AI assistant and figure out what's the best service for you for that.

In our case, I'll use:

- Prometheus for metrics
- Loki for logs
- Tempo for traces
- Grafana for displaying the dashboards

Previously I never used Loki or Tempo, but when I was telling my coding agent what I wanted to do, it suggested these technologies to me. I looked them up, read about them, and concluded that they work well for this application.

So let's implement it:

```text
Add an OpenTelemetry Collector.

Create an observability/ directory with Docker Compose for:

- OpenTelemetry Collector
- Prometheus
- Loki
- Tempo
- Grafana

Keep this as a separate Compose project from the application stack.
```

We don't have any dashboards yet, so let's build one.

## Metrics

With OTel we can collect infrastructure metrics, but it's not enough to understand what is failing in the application.

That's a good start, but it won't let us know what exactly is failing. We need to have more information about the health of our application.

We also need to collect important metrics.

For System Design Canvas, useful measurements may include:

- Total number of interview rooms
- Number of active rooms and number of active participants
- Number of elements on the canvas across the application
- Change propagation delay: when I add an element to the canvas, how long does it take for you to see it
- Number of errors


Let's start collecting them too:

```text
Track these application metrics:

- interview rooms created
- active interview participants
- canvas elements created

Display these metrics in Grafana and include the environment and deployed
version.
```


After that, we can ask the assistant to run Grafana for us and see the results.

If the assistant didn't create the dashboards yet, we can ask for them explicitly.

```text
Add Grafana panels for

- interview rooms created
- active interview participants
- canvas elements created
- failures in component creation

Make it possible to filter by environment and deployed version
```


TODO picture of grafana

Next, you can run it locally with:

```bash
docker compose -f observability/docker-compose.yaml up -d
```

We can test it by opening our application, creating a room, adding a canvas element, and checking that it appears in Grafana.


## Deploy the observability stack

We verified that it works locally, so let's now deploy it. If you use the same stack as me (Prometheus, Grafana and others), we need to deploy and manage them ourselves.

If you use a managed OTel-compatible vendor, you can skip this step. You can also use a hosted
service such as CloudWatch, Grafana Cloud, Datadog, or Sentry.


Let's deploy it:

```text
Deploy the observability stack separately from the application stack.
Connect both development and production to it.
Keep the environment and deployed version on every metric, trace, and log.
```

After it finishes, you can open Grafana and perform the same test as you did locally.

In practice, you don't deploy Grafana and Prometheus openly on the Internet. Like databases, you typically hide them behind a VPC to make sure only authorized users can access them.

## Alerting

We have the dashboards but we can't watch them all the time to see if some metrics drop or grow too large. If this happens, we have a system that triggers an alert saying that something happened.



```text
Add an actionable alert for repeated canvas component-creation failures.

Use a threshold and duration that represent real user impact. Include the
service, environment, deployed version, owner, and dashboard URL in the alert.
```

## On-Call Engineer

Now that we have alerts, we need to react to them. In companies there's usually an on-call engineer. That's the engineer who receives the alert when something happens. When it happens, they need to figure out what's happening, and find a quick solution to this problem to stop the problem.

Our AI assistant can be the on-call engineer, and if something happens, it can try to fix it. In real scenarios, AI on-call agents also need to understand if the issue is serious enough to escalate the alert to a human on-call engineer.

In our case, we won't do it. We will implement a system that checks Prometheus and Grafana for alerts, and if something is happening, an agent session will start and fix the problem.


```text
Add an on-call-engineer/ directory with a script that polls the observability
alert API every minute.

When an alert fires, pass the alert details to a headless coding agent.
```

As a result, we have a worker that polls for alerts and starts an agent session when one fires.

In my case, the agent had this prompt:

Note that for this agent you may want to limit the access to the bare minimum: logs and the repository. When it finds the fix, it pushes it to main, so the fix gets deployed. It can also trigger a manual deploy to prod if you trust your process.

```text
You are the on-call engineer for this repository. An alert just fired.

Investigate the root cause. Read the code and reproduce the failure.
If you find a real bug, make the smallest correction, run the backend tests,
and commit the fix with a clear message.
If the alert is a false positive, explain why and do not change the code.
```

<figure>
  <img src="images/04-operate-app-overview.svg" alt="A user-visible alert becomes an evidence packet for a bounded investigation; a reproducible bug produces a tested fix for CI/CD, while an uncertain case stops for explanation or escalation">
  <figcaption>A bounded agent commits only a reproducible, tested fix; otherwise it explains or escalates without changing code</figcaption>
</figure>

This is a small proof-of-concept script. In reality, you will probably have a system that looks like this:

- An alert is triggered and sent via SNS or a similar service.
- A Lambda reacts to that alert and starts a container job.
- The job launches Codex or Claude in headless mode.
- Once the session is over, the logs are saved and the machine is terminated.

TODO picture

Let's test it by introducing a bug.

## Introducing a bug

We want to test that this system works, so let's start a coding agent to introduce a bug or find an existing one.

```text
Introduce a realistic bug in canvas component creation.

For some requests, creating a component should fail even though the existing
tests pass. Keep the failure reproducible so we can test the alert and the
on-call response.
```

Here, the goal is to debug the process and make sure our on-call engineer actually wakes up and solves the problem.

After a few iterations, it will work.

TODO screenshot


## Summary



## Clean up

After you finish everything for the module, I recommend cleaning up everything. We created these things for learning, so we shouldn't forget to clean them up. If you don't, expect a bigger bill at the end of the month.

Ask your agent to clean the infra:

```text
Delete the CloudFormation stacks.
```

After it finishes, make sure everything is indeed gone. You may want to double-check everything in the AWS console or ask another agent to scan the running resources in your account.



## Next steps after this module

We now have a narrow operating baseline. We can promote a change deliberately,
observe one important user journey, and prepare a response to a known failure.
We can extend it in stages rather than add every practice in one go.

![Reliability, safer delivery and security evidence rest on the current operating baseline and support agent governance, where authority expands last.](images/04-next-steps-roadmap.svg)

Start with reliability by defining an SLI and SLO for an important journey such
as canvas sync. Add an error-budget burn-rate alert and an external synthetic
check so we notice when the app or the monitoring path fails.

Then make deployments safer with canaries or progressive rollouts, feature
flags for risky changes, and the previous release ready for rollback. Restore
a database backup because an untested backup is only a promise.

Then broaden the security evidence by scanning dependencies, secrets,
containers, and infrastructure code. Generate an SBOM and build provenance.
Add manual penetration testing and a clear path for vulnerability reports.

Raise agent autonomy last by recording what the on-call agent can read and
write and what enforces each limit. Test model upgrades against past incidents.
Widen the blast radius only when incident records show that the narrower
version is repetitive, bounded, and independently verifiable.

If we add one thing, start with an SLI and SLO for the app's most important
journey. That tells us which failures matter before we add more dashboards,
alerts, or agents.


## Next in the series

With these pieces, we can promote a change deliberately, see a failure, and
investigate it within a bounded workflow.

In the next module, we cover these coding-agent capabilities:

- MCP
- skills
- commands
- plugins
- specialized agents

We apply the same boundaries there too. Every new capability should have a
clear owner, permissions, data path, and review process.

You can find the course materials and the next cohort in
[AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp).
It's free.
