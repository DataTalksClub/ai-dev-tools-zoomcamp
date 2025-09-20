# Module 4 — Implement Our Own Agent (Django + OnePrompt-Style Template)

## Overview

- Build an agent that can safely modify a Django app based on goals.
- Architecture: planner, tools, memory, constraints/guards.
- Coupling the agent to the codebase (file IO, tests, migrations, templates).
- Developer UX: diffs, approvals, rollbacks, evals.

## Detailed Description

- Bootstrap: Django template (auth, CRUD, templates), clear local dev loop (poetry/uv/pipenv).
- Agent core: choose framework (LangGraph, PydanticAI, or lightweight custom), implement tools:
  - Filesystem patch, test runner, migration runner, git ops (branch/commit).
- Guardrails: regex/file allowlists, AST-aware edits, unit test gateways, human-in-the-loop approvals.
- Tasks: "add profile page", "paginate list view", "fix failing test", "add DRF endpoint".
- Observability: structured logs, traces, prompt templates, evaluation harness (task success rate).
- Deliverable: agent CLI that implements a feature with tests + PR creation in a demo repo.

## Relevant Links

- [Django — Docs](https://docs.djangoproject.com/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [PydanticAI](https://ai.pydantic.dev/)
- [pytest-django](https://pytest-django.readthedocs.io/)
- [GitPython](https://gitpython.readthedocs.io/)