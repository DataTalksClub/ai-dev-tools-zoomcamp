# Article 3 live workshop

Locator: `https://www.youtube.com/watch?v=gxt5ZDVnBMM`

The August 10 workshop applies the draft Article 3 sequence to the
interview-canvas application and supplies the actual prompts, checks, cloud
decisions, and failures for the post-workshop revision.

- [FACT article-3-live-workshop] The walkthrough starts with `npm run dev` for
  the frontend and `make run` for the backend, then builds one multi-stage
  image and adds a named SQLite volume so data survives container restarts.
- [FACT article-3-live-workshop] The Postgres check sets
  `SDIP_DATABASE_URL`, restarts the backend, and confirms the data remains.
- [FACT article-3-live-workshop] Compose adds a Postgres health check and waits
  for the database before starting the app. The app moves to host port 8100
  because port 8000 is already occupied.
- [FACT article-3-live-workshop] Playwright automates the same two-browser flow
  used for manual checks: interviewer login, session creation, candidate join,
  candidate canvas edit, and interviewer verification.
- [FACT article-3-live-workshop] The AWS walkthrough chooses EC2 plus Docker
  Compose and requires CloudFormation so every resource can be reviewed and
  deleted together.
- [FACT article-3-live-workshop] The live proof of concept keeps Postgres on
  the EC2 volume. The author recommends managed RDS and backups for an
  application whose data matters.
- [FACT article-3-live-workshop] The author reviews the generated resources,
  asks for a cost estimate, checks the real bill later, and watches the agent
  while it has temporary admin access.
- [FACT article-3-live-workshop] GitHub Actions runs backend and frontend jobs
  first, then integration and end-to-end tests, and finally deployment. OIDC
  replaces long-lived AWS keys with a restricted role.
- [FACT article-3-live-workshop] The cleanup stack name is `sdip`, not
  `interview-canvas`.

Limitations: YouTube subtitles contain transcription errors, so exact commands
and post-session fixes were checked against the final repository and GitHub
Actions logs. The recording ends while the deployment workflow is still being
fixed; the repository contains the completed fix.

Session date: 2026-08-10. Captured: 2026-08-12.
