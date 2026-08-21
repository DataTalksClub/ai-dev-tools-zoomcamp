# Article diagram review notes

These notes record the corrections made while reviewing Article 3, including
follow-up fixes found during rendering. Reuse them for future article diagrams.

## Workflow

- Commit the workshop text before editing it. Keep later visual changes
  uncommitted so they remain easy to review.
- Change article copy as little as possible. Captions should state the main
  idea at a high level, with only the detail needed to understand the figure.
- Keep editable JSON next to every generated SVG and PNG. Regenerate both
  formats after the last source change.
- Inspect every PNG at full resolution and iterate on anything that merely
  renders correctly but still looks awkward.
- Use the diagram rubric and an independent visual review. Do not call a figure
  10/10 without naming what was checked.

## Layout and connectors

- Align peer cards to exact rows and columns. Use equal gutters and consistent
  card sizes; peer cards never differ in size. A full-width baseline or cap
  card that spans its peers (as in the next-steps stack) is deliberate
  meaning and fine - but at most one per figure.
- Prefer straight horizontal or vertical arrows. When a flow must turn, use a
  deliberate 90-degree elbow instead of an inclined segment. Use curves only
  when they make a relationship materially clearer.
- Give arrows enough length to read clearly, and make equal relationships use
  equal arrow lengths.
- Connect arrows to the visible ink of standalone icons, not to transparent
  icon bounds. Browser, user, database, and volume connectors must visibly
  touch their symbols.
- Use separate side anchors when two inputs enter the same card so arrowheads
  do not overlap.
- Use dashed edges for secondary control actions and dashed boundaries for
  infrastructure or runtime containment.

## Icons and boundaries

- Keep icon stroke weights consistent. Browser and database symbols should not
  look heavier or lighter than the rest of the diagram.
- Use the AWS icon for AWS deployment, not the GitHub icon.
- Show a running Postgres service as a container card. Show persistent
  `pgdata` as a database cylinder. Do not add a second cylinder that duplicates
  the Postgres service.
- Use the same cylinder convention for persistent volumes throughout the
  article.
- Show CloudFormation as management context in the EC2 boundary label, not as
  an ordinary runtime node.
- Put components that run together inside a dashed container or instance
  boundary.

## Figure-specific patterns

### Development and production

- Explain the apparent two-container choice before simplifying it: development
  has separate frontend and backend services because the Vite development
  server supports the frontend workflow. In production, the frontend is static
  files served by FastAPI, so React and FastAPI share one application
  container.
- Keep the three stages visually distinct and use long, evenly spaced arrows.
- Label the SQLite cylinder as a database in this architecture view; the
  storage volume is an implementation detail and is not a separate component.

### Docker Compose and Postgres

- Keep the application visually unchanged while showing SQLite replaced by a
  Postgres service and persistent volume.
- Make the transition arrows long enough to be obvious, and use the volume
  cylinder consistently.

### Playwright test flow

- Separate automation from application traffic: dashed edges run from the top
  and bottom of Playwright to the left side of the two browser sessions.
- Solid edges run from the right side of each browser to the top and bottom of
  the shared room.
- Route these four relationships as symmetric 90-degree elbows. Keep Shared
  room to FastAPI horizontal and FastAPI to Postgres exactly vertical.

### AWS deployment

- Put Caddy, the application, Postgres, and `pgdata` inside one dashed EC2
  boundary. Caddy handles HTTPS in front of the app.
- Use a container card for Postgres and a cylinder for `pgdata`.

### CI/CD

- Use a horizontal flow to save vertical space. Show frontend and backend tests
  in parallel, then full-stack checks, then deployment.
- Keep arrows large enough to read, preserve card-title alignment, and use the
  AWS icon only on the AWS deployment node.

### End-state architecture

- Do not mix the article's implementation steps with the final architecture.
- Show two distinct browser sessions, then Caddy, one compact `React + FastAPI`
  app container, Postgres, and the `pgdata` volume inside the managed EC2
  boundary.
- Leave WebSocket details out of this summary figure when they do not help the
  reader understand the end state.

### Next lesson

- Center the user between the two action targets, not merely on the canvas.
  Show the user's push to main and manual production promotion as dashed action
  arrows of equal length.
- Connect Development and Production with a dashed line without an arrowhead.
  The user's dashed action arrow identifies who performs the promotion.
- Split operations into separate `Observe` and `Respond` boundaries.
- Show Production to Collector to Observability to Alerting to AI agent, then a
  dashed fix path back to Code.
- Align Code and AI agent in one column, Production and Collector in another,
  and keep every row internally aligned.
