# Article 3 provenance report

Target: `articles/03-deployment.md`

Rendered: 2026-08-09
Post-live revision: 2026-08-12

## Claim map

- The Article 2 recap, application behavior, SQLAlchemy boundary, and promised
  deployment topics come from `article-2-end-to-end`.
- The container → Postgres → Compose → AWS → CI/CD → cleanup sequence comes from
  `article-3-live-workshop` and is cross-checked against the final repository.
- `SDIP_DATABASE_URL`, ports 8000 and 8100, Compose health checks, all four test
  suites, the CloudFormation stack, and the finished workflow come from
  `interview-canvas-repository` at commit `e536482`.
- CloudFront WebSocket forwarding guidance comes from the official AWS CloudFront
  documentation retrieved on 2026-08-09.
- GitHub Actions OIDC and repository/branch trust restrictions come from the
  official AWS IAM and GitHub Actions documentation retrieved on 2026-08-09.

## Certainty audit

- The existing container section describes repository code that exists at the
  captured commit.
- Postgres, Compose, integration-test, CloudFormation, and GitHub Actions files
  exist in the post-workshop repository and are linked as verified outputs.
- The article does not claim a live public URL.
- AWS service behavior is supported by current official documentation, but a
  generated CloudFormation template will still require a code-level review and
  live deployment test.

## Approved deviations

- The author asked to start Article 3 with containerization, so integration
  tests follow Postgres and Compose.
- The author asked to skip migrations. The article keeps a short caveat that
  startup table creation is only suitable for a new proof-of-concept database.
- The Snake Royale identifiers and build workaround from the workshop were
  replaced with interview-canvas names and the repository's actual
  `dist/client` output.

## Human edit reminders

- Add screenshots or diagrams only after the actual deployed interview-canvas
  flow has been captured.
