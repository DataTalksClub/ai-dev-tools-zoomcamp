# Module 4 Tool-Agnostic Security, Audit, and DevOps Curriculum

## Intended reader

Learners in the 2026 AI Dev Tools Zoomcamp who have already built an application and extended a coding agent in Modules 2 and 3. They may use Codex, Claude Code, or another terminal coding agent.

## Desired change

Learners should understand durable security, audit, and operations concepts rather than memorize a curated list of products. They should be able to implement the same workflows with different coding agents and ordinary command-line tools, including interactive or headless execution.

## Core claim

Module 4 should be concept-first and tool-agnostic. Named products can be examples, but each lesson should teach a transferable workflow that learners can reproduce with a terminal coding agent such as Codex or Claude Code plus standard CLI tooling.

## Brain dump

The existing Module 4 may actually be too focused on tools. First inspect what tools it proposes and identify the underlying concepts it is trying to teach. Map those concepts into an article so we can discuss the curriculum before deciding exactly how to implement the labs.

The desired sequence is:

1. Inventory the current tools and lessons.
2. Extract and organize the durable concepts.
3. Research which concepts matter and which can be implemented ourselves.
4. Propose a concept-first article/module structure.
5. Only after discussion, design concrete implementations that work with Codex, Claude Code, and comparable agents in terminal/CLI or headless mode.

## Must use

- The current `04-ai-security-audit-devops/README.md` and the related Module 4 section of `docs/2026-syllabus-proposal.md` as evidence of current intent.
- The user's judgment that portability across Codex and Claude Code is a primary requirement.
- The course's repo-centered, hands-on teaching style.

## Must avoid

- Organizing the curriculum around product names.
- Requiring one proprietary coding-agent interface or vendor-specific extension format.
- Treating probabilistic AI output as authoritative security or operational evidence.
- Implementing the labs before the concept map and teaching direction have been discussed and approved.

## Constraints

- This pass is research and curriculum design, not lab implementation.
- The eventual article should be practical, concise enough to teach, and explicit about concepts, evidence, human approval, and verification.
- Examples may name tools, but the core workflow must transfer across terminal coding agents and standard CLI/headless environments.
