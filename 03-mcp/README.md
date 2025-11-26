# Module 3 — MCP Deep Dive & Agents (Developer-Centric Servers)

Videos:

* [▶️ Watch the Workshop Video](https://www.youtube.com/watch?v=0IhZdcjddo4&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)
* [Working Demo](https://www.youtube.com/watch?v=HYHv_S141CU&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)

> Note: during the live stream we had some problems with the demo. Check the "Demo" for the working version.

## Overview

- How MCP standardizes tool access for LLMs/agents.
- Core servers developers actually use: GitHub, Filesystem, DB/SQL, HTTP/API, CI.
- Practical workflows: repo triage, PR summarization, scripted edits, data queries.
- Security/permissions, auditing, and local vs. remote servers.

## Detailed Description

- MCP concepts: tools/resources/prompts; capabilities vs. classic API keys; connection flows.
- Server survey & demos:
  - GitHub (issues/PRs/contents), Filesystem (read/write/patch), Database (Postgres/MySQL),
    HTTP/Fetch (call any OpenAPI), CI (Actions/GitLab), and productivity (Notion/Slack/Zapier MCP).
- Building a minimal MCP workflow: list PRs → fetch diff → suggest changes → open issue/PR.
- Safety: scopes, read-only vs. write, logging, approving write operations, secrets handling.
- Deliverable: "Repo Assistant" that chains GitHub + Filesystem (read/patch) with a review checklist.

## Relevant Links

- [Model Context Protocol — Site](https://modelcontextprotocol.io/)
- [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol)
- [GitHub MCP Server (example implementation)](https://github.com/search?q=github+mcp+server&type=repositories)
- [Awesome MCP (community lists)](https://github.com/search?q=awesome+mcp&type=repositories)
- [Zapier — AI Actions / MCP](https://zapier.com/labs/ai-actions)