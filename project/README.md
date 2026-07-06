# Final Project

> [!NOTE]
> The 2026 project requirements are currently a draft. You can use this page to see what we are preparing, but the final project rules, scoring, deadlines, and peer-review requirements may change before the cohort starts.

The final project applies the full course workflow to an end-to-end application of your own.

You will:

- build and deploy a full-stack app with AI assistance
- document how AI tools were used and reviewed
- add an agent extension pack around the project
- audit and harden the project with open-source AI security, audit, and DevOps tools
- review peer projects

## Expected Repository Contents

Your project repo should include:

```text
README.md
product-spec.md
AGENTS.md or equivalent project instructions
frontend/
backend/
openapi.yaml
docker-compose.yml
.github/workflows/
docs/
security/
ops/
```

If you complete Module 3, it should also include an agent extension pack:

```text
agent-capabilities/
agent-hooks/
mcp-server/
plugins/ or custom-agent/
docs/agent-extension-pack.md
docs/permissions.md
```

## Peer Reviewing

> [!IMPORTANT]
> To evaluate projects, we use peer review. To get points for your project, you need to evaluate projects from your peers. Final peer-review requirements for the 2026 cohort are still being prepared.

## Draft Criteria

### 1. Problem Description

- The problem is not described. (0 points)
- The problem is described briefly, but it is unclear what the system does or what functionality is expected. (1 point)
- The README clearly describes the problem, the system functionality, and expected behavior. (2 points)

### 2. AI-Assisted Development Workflow

- No description of how AI tools were used. (0 points)
- The project describes how AI tools were used to build the system. (1 point)
- The project clearly documents the AI workflow, including prompts or task delegation, context files, manual review, and verification. (2 points)

### 3. Technologies and System Architecture

- Technologies are not described or are unclear. (0 points)
- The main technologies are mentioned, but their roles are not explained. (1 point)
- The project clearly describes the frontend, backend, database, containerization, CI/CD, and how they fit together. (2 points)

### 4. Frontend Implementation

- No frontend or non-functional frontend. (0 points)
- A functional frontend exists, but structure is unclear or backend calls are scattered. (1 point)
- The frontend is functional and well structured, with centralized backend communication. (2 points)
- The frontend is functional, well structured, and includes tests covering core logic, with clear instructions for running them. (3 points)

### 5. API Contract

- No OpenAPI specification. (0 points)
- OpenAPI specification exists but is incomplete or loosely aligned with frontend needs. (1 point)
- OpenAPI specification reflects frontend requirements and is used as the contract for backend development. (2 points)

### 6. Backend Implementation

- No backend or backend does not follow the API contract. (0 points)
- Backend implements required endpoints but has limited structure or documentation. (1 point)
- Backend is well structured and follows the OpenAPI specification. (2 points)
- Backend is well structured, follows the OpenAPI specification, and includes tests covering core functionality. (3 points)

### 7. Database Integration

- No database or persistent storage. (0 points)
- Database is integrated, but configuration or usage is minimal or poorly documented. (1 point)
- Database layer is properly integrated, supports different environments, and is documented. (2 points)

### 8. Containerization

- No containerization. (0 points)
- Dockerfiles exist, but running the full system requires manual steps. (1 point)
- The full system runs via Docker or Docker Compose with clear instructions. (2 points)

### 9. Integration Testing

- No integration tests. (0 points)
- Integration tests exist but are limited or not clearly separated from unit tests. (1 point)
- Integration tests are clearly separated, cover key workflows, and are documented. (2 points)

### 10. Deployment

- Application is not deployed. (0 points)
- Deployment steps are described, but no working deployment is shown. (1 point)
- Application is deployed to the cloud with a working URL or clear proof of deployment. (2 points)

### 11. CI/CD Pipeline

- No CI/CD pipeline. (0 points)
- CI pipeline runs tests automatically. (1 point)
- CI/CD pipeline runs tests and deploys the application when tests pass. (2 points)

### 12. Agent Extension Pack

- No agent extension work is included. (0 points)
- The project includes basic project instructions or reusable prompts. (1 point)
- The project includes a documented extension pack with project instructions, a reusable workflow, a subagent/specialist, an MCP tool/server, a hook or guardrail, and permission notes. (2 points)

### 13. Security, Audit, and DevOps Hardening

- No security/audit/DevOps review artifacts. (0 points)
- The project includes at least one audit or security scan artifact. (1 point)
- The project includes PR audit output, deterministic security scan findings, agent/extension security notes, operational diagnosis output, and an AI tool/data policy. (2 points)

### 14. Reproducibility

- Project cannot be run with the provided instructions. (0 points)
- Project can be run, but setup or run instructions are incomplete. (1 point)
- Clear instructions exist to set up, run, test, and deploy the system end to end. (2 points)

## Previous Cohort Materials

The previous project requirements are archived here:

- [2026 archived project page](../cohorts/2026/project/)
