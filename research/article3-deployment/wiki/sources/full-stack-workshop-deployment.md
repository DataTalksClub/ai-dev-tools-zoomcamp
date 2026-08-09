# Full-stack workshop deployment chapters

Locator: `/home/alexey/git/ai-shipping-labs-workshops-raw/2026/06/2026-06-23-full-stack-vibe-coding`

Chapters 10–16 document the deployment half of the workshop linked from Article
2. The workshop uses a Snake Royale application, so its process is reusable but
its identifiers and a few implementation details are not.

- [FACT full-stack-workshop-deployment] Chapter 10 creates one multi-stage image
  containing a compiled frontend and FastAPI backend, then verifies it through
  the exposed port.
- [FACT full-stack-workshop-deployment] Chapters 11 and 12 introduce Postgres and
  Compose, including a named volume, service networking, and readiness health
  check.
- [FACT full-stack-workshop-deployment] Chapter 13 deploys with CloudFormation,
  managed Postgres, Secrets Manager, EC2, HTTPS, and a public URL.
- [FACT full-stack-workshop-deployment] Chapter 14 gates deployment behind tests
  and authenticates GitHub Actions to AWS through OIDC.
- [FACT full-stack-workshop-deployment] Chapter 15 deletes the chargeable AWS
  stack.
- [FACT full-stack-workshop-deployment] Deferred work includes database
  migrations and production hardening.

Limitations: the workshop's environment variables, paths, application behavior,
and Docker build workaround belong to Snake Royale. Its approximate mid-2026
cost figures are time-sensitive and unnecessary for this article.

Published: 2026-06-23. Captured: 2026-08-09.
