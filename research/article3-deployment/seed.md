# Article 3: Deploying the Interview Canvas App

## Intended reader

Readers of the AI Dev Tools Zoomcamp article series who followed Article 2 and
now have the interview-canvas application working locally.

## Desired change

Show the reader how to take the exact Article 2 application from a local
FastAPI/React/SQLite setup to a containerized, tested, deployed application
with an automated CI/CD path.

## Core claim

Deployment should continue Article 2's incremental AI-assisted workflow: ask
for one bounded change, run the result, diagnose failures with evidence, and
only then move to the next layer.

## Brain dump

Article 3 is currently an incomplete fragment that begins with integration
tests and containers. The rest of the material lives in the full-day AI
Shipping Labs workshop linked from Article 2. That workshop uses Snake Royale,
but this article must translate every relevant example to the system-design
interview application from Article 2. Likely sequence: introduction and recap;
integration tests; one Docker image for frontend and backend; Postgres; Docker
Compose; cloud deployment; GitHub Actions CI/CD; cleanup and conclusion.

## Must use

- `articles/02-end-to-end.md` for the running example, voice, and handoff.
- `articles/03-deployment.md` for the existing fragment that must be completed.
- The June 23 full-stack workshop in `../ai-shipping-labs-workshops-raw` for the
  deployment sequence, prompts, failure observations, and operational details.
- The current `interview-canvas-share` repository for actual names and project
  structure.

## Must avoid

- Do not switch back to the workshop's Snake Royale example.
- Do not invent commands, environment variable names, paths, or cloud files
  that the interview-canvas repository does not support without labeling them
  as prompts or proposed outputs.
- Do not turn the article into a generic catalog of deployment platforms.
- Do not copy workshop prose mechanically; adapt it into one cohesive article.

## Constraints

Markdown article at `articles/03-deployment.md`. Match Article 2's direct,
practical, first-person teaching voice and prompt-driven structure. Keep enough
technical detail for readers to repeat the process, but link to the workshop
for the exhaustive walkthrough. Preserve user-authored wording where useful
and fix obvious typos in newly written prose. No web research beyond the
referenced repository is necessary unless a technical gap cannot be resolved
locally.
