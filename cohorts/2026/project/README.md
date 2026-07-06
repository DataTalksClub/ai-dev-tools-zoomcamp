## Projects 

[Video: Submit and evaluate Zoomcamp projects 🎥](https://www.loom.com/share/4f5c155c550e48ddb54b71ba76516b04)


The idea is that you now apply everything we learned so far yourself.

There are two projects in this course

* Attempt 1
* Attempt 2

You only need to complete one (but you can do both if you have time and energy).


This is what you need to do for each project:

* Think of a problem that's interesting for you
* Describe this problem
* Create the frontend, backend and describe their communication with API specs
    * You can do it in any order:
    * Frontend first, like shown in the course
    * Specs first 
    * Backend first
    * But all three have to be done
* Make sure the application is thoroughly tested, containerized and deployed
* Make sure you review your peers - or you won't get a certificate of graduation 


## Peer reviewing

> [!IMPORTANT]  
> To evaluate the projects, we'll use peer reviewing. This is a great opportunity for you to learn from each other.
> * To get points for your project, you need to evaluate 3 projects of your peers
> * You get 3 extra points for each evaluation
> * If you don't evaluate your peers, you fail the project


## Criteria 

1. Problem description (README)
- The problem is not described. (0 points)
- The problem is described briefly, but it is unclear what the system does or what functionality is expected. (1 point)
- The README clearly describes the problem, the system’s functionality, and what the project is expected to do. (2 points)

2. AI system development (tools, workflow, MCP)
- No description of how the system was built or how AI tools were used. (0 points)
- The project describes how AI tools were used to build the system (e.g. coding assistants, prompts, workflows, AGENTS.md or similar guidance). (1 point)
- The project clearly documents AI-assisted system development and additionally describes how MCP was used (e.g. MCP server, tools, or workflow). (2 points)

3. Technologies and system architecture
- Technologies used in the project are not described or are unclear. (0 points)
- The main technologies are mentioned (e.g. frontend framework, backend framework, database), but without explaining their roles. (1 point)
- The project clearly describes the technologies used (frontend, backend, database, containerization, CI/CD) and explains how they fit into the system architecture. (2 points)

4. Front-end implementation
- No front-end or non-functional front-end. (0 points)
- A functional front-end exists, but structure is unclear or backend calls are scattered. (1 point)
- Front-end is functional and well-structured, with centralized backend communication. (2 points)
- Front-end is functional, well-structured, and includes tests covering core logic, with clear instructions on how to run them. (3 points)

5. API contract (OpenAPI specifications)
- No OpenAPI specification. (0 points)
- OpenAPI specification exists but is incomplete or loosely aligned with front-end needs. (1 point)
- OpenAPI specification fully reflects front-end requirements and is used as the contract for backend development. (2 points)

6. Back-end implementation
- No back-end or back-end does not follow the API contract. (0 points)
- Back-end implements required endpoints but has limited structure or documentation. (1 point)
- Back-end is well-structured and follows the OpenAPI specifications. (2 points)
- Back-end is well-structured, follows the OpenAPI specifications, and includes tests covering core functionality, clearly documented. (3 points)

7. Database integration
- No database or persistent storage. (0 points)
- Database is integrated, but configuration or usage is minimal or poorly documented. (1 point)
- Database layer is properly integrated, supports different environments (e.g. SQLite and Postgres), and is documented. (2 points)

8. Containerization
- No containerization. (0 points)
- Dockerfiles exist, but running the full system requires manual steps. (1 point)
- The entire system runs via Docker or docker-compose with clear instructions. (2 points)

9. Integration testing
- No integration tests. (0 points)
- Integration tests exist but are limited or not clearly separated from unit tests. (1 point)
- Integration tests are clearly separated, cover key workflows (including database interactions), and are documented. (2 points)

10. Deployment
- Application is not deployed. (0 points)
- Deployment steps are described, but no working deployment is shown. (1 point)
- Application is deployed to the cloud with a working URL or clear proof of deployment. (2 points)

11. CI/CD pipeline
- No CI/CD pipeline. (0 points)
- CI pipeline runs tests automatically. (1 point)
- CI/CD pipeline runs tests and deploys the application when tests pass. (2 points)

12. Reproducibility
- Project cannot be run with the provided instructions. (0 points)
- Project can be run, but setup or run instructions are incomplete. (1 point)
- Clear instructions exist to set up, run, test, and deploy the system end-to-end. (2 points)
