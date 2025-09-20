# Module 2 — End-to-End Game (Snake) with OpenAPI-First + FastAPI

## Overview

- Frontend-first: build Snake in React/TS (or vanilla JS) with clean state & input loops.
- OpenAPI-first design for the backend contract.
- Generate FastAPI server from spec; add handlers/tests.
- Integrate FE/BE via typed SDKs/clients.

## Detailed Description

- Frontend: board & snake state, tick loop, collision/food logic, scoring; design clean interfaces.
- API design: sketch interactions (scores, leaderboards, user profile), write OpenAPI 3.1 spec.
- Codegen: server stubs with OpenAPI Generator or fastapi-code-generator; add pydantic models.
- Backend: implement handlers, auth (token or session), persistence (SQLite/Postgres), CORS.
- Client: generate/handwrite a typed API client; integrate into React with hooks/swr.
- Testing: FE unit tests (vitest/jest), BE tests (pytest), contract tests vs. the spec.
- Deliverable: deployed game (Vercel/Render) + spec + CI that validates spec and tests.

## Relevant Links

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [OpenAPI Generator (servers/clients)](https://openapi-generator.tech/)
- [fastapi-code-generator](https://pypi.org/project/fastapi-code-generator/)
- [FastAPI — Docs](https://fastapi.tiangolo.com/)
- [TypeScript + React — Official Docs](https://react.dev/learn/typescript)
- [Vitest](https://vitest.dev/)
- [Pytest](https://docs.pytest.org/)