# Guideline

Status: proposed article plan

## Reader and promise

Write for two overlapping readers: someone deciding whether to join and a registered learner asking “what do I do now?”

Promise: in one article, the reader will understand the learning journey, how the cohort works, and the exact canonical destination for every next action.

## Thesis

The AI Dev Tools Zoomcamp is a coherent AI-native software-engineering journey: specify the work, build the application, ship it safely, operate it with evidence and guardrails, and extend the agents around it. It is delivered through the free Zoomcamp cohort format. [INFERENCE current-course-repository,previous-launch-video]

Non-goals:

- Do not compare the course with previous editions or include a “what changed” section.
- Do not duplicate detailed rules or deadlines that already have canonical homes.
- Do not imply that “live cohort” means weekly live lectures.

## Recommended title and deck

Title: “AI Dev Tools Zoomcamp 2026: From Idea to Production with AI Coding Agents”

Alternative: “The New AI Dev Tools Zoomcamp: AI-Native Software Engineering from Spec to Production”

Deck: “Learn one end-to-end AI-native engineering workflow, from specification to production. Here is what you will learn, how the cohort works, and where to start.”

## Ordered outline

### 1. Launch-day opening (100 to 150 words)

Open with the course starting on August 31, the fact that it is free, and the end-to-end learning promise. Use one primary CTA: start on the course platform. Follow with secondary links to the repository and docs. [FACT live-registration-page,current-course-repository]

Avoid opening with administrative details or a history lesson.

### 2. “Start here” link block (highly scannable)

Include these actions near the top:

1. Register for email updates: https://courses.datatalks.club/register/ai-dev-tools/
2. Open/enroll in the course platform for schedule, submissions, and scores: https://courses.datatalks.club/ai-dev-tools-2026/
3. Open the current materials: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp
4. Read the course docs: https://datatalks.club/docs/courses/ai-dev-tools-zoomcamp/
5. Join Slack and the course channel: https://datatalks.club/slack.html and https://app.slack.com/client/T01ATQK62F8/C09HWT76L95
6. Join Telegram announcements: https://t.me/aidevtoolszoomcamp
7. Save the YouTube playlist: https://www.youtube.com/playlist?list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43

Explicitly state that registration for updates and the course-platform account are different. [FACT zoomcamp-docs]

### 3. The five-module journey (500 to 650 words)

Use a consistent mini-card for every module: learner problem, outcome, and three links (materials, recording, companion article where available). This makes the section useful without copying the full syllabus.

1. AI-Native Developer Workflow: turn a vague idea into a spec, durable context, backlog, implementation loop, and independent QA. Outcome: a repeatable way to direct and verify coding agents.
2. Build and Ship an AI-Assisted Full-Stack App: move from product spec through frontend, OpenAPI, backend, SQLite, and unit tests. Outcome: a tested app that runs locally.
3. Test, Containerize, and Deploy: add integration tests, Postgres, Docker, CI, public deployment, and CI/CD. Outcome: a reproducible app that ships automatically when checks pass.
4. DevOps and Observability: instrument one user journey, alert on impact, collect an evidence packet, use a read-only agent responder, enforce actions outside the model, and audit the system. Outcome: an operations and security report.
5. Coding Agent Capabilities: understand the agent loop and package instructions, MCP, skills/workflows, hooks, subagents, plugins, and custom agents with permissions. Outcome: a project-specific agent extension pack.

End this section with one sentence showing the cumulative arc: `specify -> build -> ship -> operate -> extend`.

Use the current top-level README and module pages for links and wording. [FACT current-course-repository]

### 4. How the cohort works (200 to 250 words)

Summarize only the stable mechanics:

- Lectures are pre-recorded; “live cohort” means shared deadlines, scored homework, leaderboard, community, peer review, and certificate eligibility.
- Use the repository for lessons and homework; use the platform for exact deadlines and submissions.
- Homework is optional for certification but useful for pacing, practice, and leaderboard points.
- Use Telegram for announcements and Slack for questions and discussion.
- Learners can also follow self-paced, but scoring, peer review, and certificates belong to the live cohort.

Link to the shared logistics docs instead of expanding every rule. [FACT previous-launch-video,zoomcamp-docs,current-course-repository]

Do not include a weekly time estimate until the author resolves the current 5-to-10 versus 10-to-15-hour discrepancy.

### 5. Final project and certificate (150 to 200 words)

Explain that learners build and deploy an application of their own, document how AI was directed and reviewed, and bring together the course’s testing, deployment, operations, and agent-extension practices. [FACT current-course-repository]

State the certificate rule precisely: homework is not required; passing the final project and completing the required peer reviews during the live cohort are required. Link to the project page, platform, and certification docs. [FACT current-course-repository,zoomcamp-docs]

Avoid promising the number of attempts or exact rubric until the draft warnings are resolved.

### 6. “Where everything lives” source-of-truth map (100 to 150 words)

Give one-line destinations:

- Course platform: schedule, exact deadlines, forms, submissions, scores, project, certificate.
- GitHub repository: current curriculum, recordings, code, homework, project requirements.
- Docs: durable Zoomcamp logistics and detailed how-to guidance.
- Slack: questions and learner discussion.
- Telegram: announcements and deadline changes.
- YouTube: recordings.

This is the article’s most bookmarkable section. [INFERENCE current-course-repository,zoomcamp-docs]

### 7. Closing checklist and CTA (75 to 100 words)

End with a four-step action sequence: open the platform, bookmark/star the repo, join Slack and Telegram, begin Module 1. Mention that joining after launch is still possible, but the platform is the source for remaining deadlines.

## Link policy

Link module names to their repository folders. Link logistics claims to the relevant docs pages. Link only the start date in prose; send all changing dates to the platform. Keep the registration link distinct from the platform link.

## Voice

Practical, confident, welcoming, and specific. Write as the course creator speaking to learners, using “you” and “we.” Keep paragraphs short. Prefer concrete outcomes over lists of tool names. Treat tools as examples and engineering practices as the durable subject.

Avoid hype such as “revolutionary,” “master AI,” or “10x developer.” Avoid describing the course as prompt engineering or vibe coding. Present the curriculum as a clear progression without discussing its history.

## Length

Proposed target: 1,000 to 1,400 words. If the publication venue favors shorter launch posts, compress module mini-cards before cutting the onboarding and source-of-truth sections.

## Required pre-publication checks

1. Confirm the five-module names and whether draft warnings can be removed.
2. Update or clearly supersede the stale course-specific docs curriculum and date.
3. Verify the platform link works for logged-out learners and gives a clear enrollment path.
4. Confirm the final-project and peer-review wording for 2026.
5. Decide whether to publish a course-specific workload estimate.
