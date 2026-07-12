# Module 5 — AI for CI/CD & DevOps

## Overview

- AI-assisted PR reviews/summaries and change-risk hints.
- Automated test generation, coverage gates, and LLM evals in CI.
- Release notes, changelog drafting, and deployment runbooks.
- Incident postmortems and on-call copilots.

## Detailed Description

- GitHub Actions pipeline with AI steps: PR summary, conventional commit check, test generation prompt, and release notes.
- PR review bots (open-source or SaaS) and custom prompts per repository guidelines.
- LLM evaluation & regression checks (prompt/response golden sets) to fail builds on degradation.
- Secure usage: secrets, data redaction, OSS policy for AI usage, artifact retention, audit.
- Deliverable: a repo with CI that auto-summarizes PRs, generates draft tests, and composes release notes on tag.

## Relevant Links

- [GitHub Actions — Docs](https://docs.github.com/actions)
- [GitHub Copilot for Pull Requests](https://docs.github.com/copilot/using-github-copilot/pull-requests)
- [CodeRabbit AI PR Reviewer (Action)](https://github.com/marketplace/actions/coderabbit-ai-pr-reviewer)
- [Evidently — LLM Evaluation](https://www.evidentlyai.com/llm-evaluation)
- [Deepchecks LLM](https://docs.deepchecks.com/stable/llm/index.html)