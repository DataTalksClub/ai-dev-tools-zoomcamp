<p align="center">
  <img width="100%" src="images/course-cover.png" alt="AI Dev Tools Zoomcamp Cover Image">
</p>

<h1 align="center">
    AI Dev Tools Zoomcamp: AI-Native Software Engineering
</h1>

<p align="center">
A free course on building, extending, auditing, and operating software with AI developer tools.
</p>

<p align="center">
<a href="https://courses.datatalks.club/register/ai-dev-tools/"><img src="https://user-images.githubusercontent.com/875246/185755203-17945fd1-6b64-46f2-8377-1011dcb1a444.png" height="50" /></a>
</p>

<p align="center">
<a href="https://datatalks.club/slack.html">Join Slack</a> •
<a href="https://app.slack.com/client/T01ATQK62F8/C09HWT76L95">#course-ai-dev-tools-zoomcamp Channel</a> •
<a href="https://t.me/aidevtoolszoomcamp">Telegram Announcements</a> •
<a href="https://www.youtube.com/playlist?list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43">Course Playlist</a> •
<a href="https://datatalks.club/faq/ai-dev-tools-zoomcamp.html">FAQ</a>
</p>

<p align="center">
<a href="https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge" /></a>
<a href="https://datatalks.club/slack.html"><img src="https://img.shields.io/badge/Slack-Join%20Community-4A154B?style=for-the-badge&logo=slack" /></a>
</p>

> [!NOTE]
> The 2026 materials are currently a draft. You can use this repository to see what we are preparing for the next cohort, but the final content, videos, homework, deadlines, and project requirements may change before the cohort starts.

## Quick Links

| Resource | Link |
|----------|------|
| Registration | [Sign up for the 2026 cohort](https://courses.datatalks.club/register/ai-dev-tools/) |
| Course materials | [GitHub repository](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp) |
| Video lectures | [YouTube playlist](https://www.youtube.com/playlist?list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43) |
| Documentation | [Zoomcamp Logistics](https://datatalks.club/docs/courses/zoomcamp-logistics/) · [AI Dev Tools Zoomcamp](https://datatalks.club/docs/courses/ai-dev-tools-zoomcamp/) |
| Course platform | [AI Dev Tools Zoomcamp 2026](https://courses.datatalks.club/ai-dev-tools-2026/) |
| Slack channel | [#course-ai-dev-tools-zoomcamp](https://app.slack.com/client/T01ATQK62F8/C09HWT76L95) |
| Announcements | [Telegram](https://t.me/aidevtoolszoomcamp) |
| FAQ | [FAQ document](https://datatalks.club/faq/ai-dev-tools-zoomcamp.html) |

## About the Course

The AI Dev Tools Zoomcamp is a free, hands-on course that teaches a practical AI-native developer workflow:

> Choose the right AI tool, give it the right context, extend it with the right capabilities, and ship safely with review, audit, security, and DevOps controls.

You'll compare modern AI developer tools, build and deploy a full-stack app, customize coding agents with MCP and reusable capabilities, and use open-source AI tools for security, audit, and operations.

## Who Should Join

This course is for anyone who wants to use AI tools to help with coding. You don't need any AI experience to start, just curiosity about using AI tools in your work.

## Prerequisites

- A basic ability to program (Python, JavaScript, or similar)
- No prior experience with AI tools is required

## How to Take the Course

There are two ways to follow the course: live and self-paced.

| | Live Cohort | Self-Paced |
|-|-|-|
| Start | August 31, 2026 | Anytime |
| Lectures | Pre-recorded | Pre-recorded |
| Homework | Graded | Available but not scored |
| Leaderboard | ✅ Yes | ❌ No |
| Peer Review | ✅ Yes | ❌ No |
| Certificate | ✅ Yes | ❌ No |
| Cost | Free | Free |
| Register | [Sign up here](https://courses.datatalks.club/register/ai-dev-tools/) | Just start learning! |

> [!IMPORTANT]
> "Live cohort" does not mean live classes. All lectures are pre-recorded. "Live" means working alongside others with deadlines, scored homework, a leaderboard, peer review, and a certificate at the end.

Self-paced steps:

1. Follow the materials on [GitHub](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp)
2. Ask questions and share progress in [Slack](https://datatalks.club/slack.html)
3. Do the homework (self-checked) and build a project for your portfolio

## Syllabus

### [Module 1: AI-Native Developer Workflow](01-overview/)

- Compare chat assistants, terminal coding agents, agentic IDEs, cloud agents, and project bootstrappers
- Learn when to use ChatGPT/Claude/Gemini-style chat, Claude Code/Codex/Gemini CLI-style terminal agents, Cursor/Windsurf/Zed/Antigravity-style IDEs, and Lovable/Bolt/Replit-style bootstrappers
- Practice context engineering with `AGENTS.md`, `CLAUDE.md`, repository instructions, product specs, architecture notes, testing guidelines, and security checklists
- Complete one small feature using a disciplined AI development loop: spec, context, plan, edit, run, test, inspect diff, review, commit

### [Module 2: Build and Ship an AI-Assisted Full-Stack App](02-end-to-end/)

- Write a product spec and acceptance criteria
- Build a frontend prototype with AI assistance
- Define the API contract with OpenAPI
- Implement a FastAPI or Django backend
- Add database support, tests, Docker, deployment, and CI/CD
- Outcome: a deployed full-stack app with tests, Docker setup, OpenAPI contract, and a reproducible development workflow

### [Module 3: Coding Agent Capabilities: MCP, Skills, Plugins, and Custom Agents](03-mcp/)

- Learn how modern coding agents are extended and customized
- Treat Claude Code, Codex, OpenCode, Cursor, GitHub Copilot, Aider, and similar tools as examples of the same broader agent workflow
- Cover project instructions, MCP, reusable workflows/skills, hooks, specialized subagents, plugins/extensions, and custom agents
- Outcome: an agent extension pack for your app, including project instructions, a reusable workflow/skill/command, a specialized subagent, a hook, an MCP tool/server, and either a small plugin/extension package or custom agent

### [Module 4: Open-Source AI Tools for Security, Audit, and DevOps](04-ai-security-audit-devops/)

- Use open-source AI tools around the production workflow
- Focus on AI PR audit, AI-accessible security scanning, agent/MCP/skill security scanning, Kubernetes diagnostics, incident investigation, and AI tool governance
- Required stack: PR-Agent, Semgrep MCP, Snyk Agent Scan, K8sGPT, LiteLLM, and Ollama
- Optional demos: HolmesGPT and Stakpak
- Outcome: a security/audit/DevOps hardening package for the final project

## Final Project

The [final project](project/) applies the course workflow to an end-to-end app of your own: build it with AI assistance, extend the coding agent around it, then audit and harden the result with security and DevOps tooling. Projects are evaluated through peer review.

## Certificate

Certificates are awarded to learners who complete the final project and the required peer reviews during a live cohort. See [Certification](https://datatalks.club/docs/courses/zoomcamp-logistics/certification/) for how certification works and how to get your certificate.

## Instructors

- [Alexey Grigorev](https://linkedin.com/in/agrigorev)
- [Bhavani Ravi](https://www.linkedin.com/in/bhavanicodes)
- [Moein Foroughi](https://www.linkedin.com/in/moein-foroughi-ce/)

## Testimonials

> This course fundamentally changed how I approach AI development. I moved from "building models" to designing AI-assisted systems that are faster to ship and easier to iterate on.
>
> During the course, I built:
>
> - A portfolio optimization tool powered by AI-assisted development
> - A full-stack application using ChatGPT, Lovable, and Antigravity
> - A structured GitHub project with clean documentation and reproducible workflow
>
> What changed for me: I now think in terms of system design rather than isolated scripts. I learned how to structure AI tool usage, validate outputs, and integrate generated code into disciplined engineering workflows. The biggest shift was moving from experimentation to controlled, production-oriented iteration. I can now prototype and deploy AI-enabled tools significantly faster without sacrificing rigor.
>
> — [Yann Pham-Van](https://www.linkedin.com/in/chasseur2valeurs/), Freelance Data Scientist

> The course taught me how to use coding agents effectively, debug issues, and gave me exposure to MCPs, tools, and prompts. It helped me conceptualize any idea into a working prototype. And finally, it helped me land a job after a long career break!
>
> — [Revathy Ramalingam](https://www.linkedin.com/in/revathy-ramalingam/), Senior Software Engineer at Yalabs Solutions

> During the course I built a Finnish learning website which helps English users learn and practice reading, writing, listening and speaking skills for the Finnish language. I used the Antigravity IDE with Gemini 3 Pro and Claude Opus, a Context7 documentation MCP server, TypeScript and Python, Next.js and FastAPI, SQLite, and CI/CD with GitHub Actions.
>
> What changed for me: learning a systematic way to think about requirements and design an application before building and testing components iteratively, packaging frontend and backend into a single container for easier deployment, and getting comfortable debugging frontend and backend tests during integration and deployment.
>
> — [Kaiquan Mah](https://www.linkedin.com/in/kaiquan-mah), Data Scientist at Total eBiz Solutions

## Community & Support

### Getting Help on Slack

Join the [#course-ai-dev-tools-zoomcamp](https://app.slack.com/client/T01ATQK62F8/C09HWT76L95) channel on [DataTalks.Club Slack](https://datatalks.club/slack.html) for discussions, troubleshooting, and networking.

To keep discussions organized:

- Follow [our guidelines](https://datatalks.club/docs/courses/zoomcamp-logistics/asking-questions/) when posting questions.
- Review the [community guidelines](https://datatalks.club/slack/guidelines.html).

### Learning in Public

Share your progress as you go, using the hashtag #aidevtools and tagging Alexey Grigorev or DataTalksClub. It helps you learn better, builds your network, and earns you bonus points. See the [learning in public guide](https://datatalks.club/docs/courses/zoomcamp-logistics/learning-in-public/).

## Sponsors

Interested in supporting our community? Reach out to [alexey@datatalks.club](mailto:alexey@datatalks.club).

## FAQ

A few common questions. For everything else, see the full [AI Dev Tools Zoomcamp FAQ](https://datatalks.club/faq/ai-dev-tools-zoomcamp.html).

Q: Is this course really free?<br/>
A: Yes. All videos, materials, and homework are free and open-source.

Q: Do I need prior experience?<br/>
A: No AI experience is needed. A basic ability to program in Python, JavaScript, or a similar language is enough.

Q: What does "live cohort" mean? Are there live classes?<br/>
A: No mandatory live classes. All lectures are pre-recorded. "Live" means deadlines, scored homework, a leaderboard, peer review, and certificate eligibility.

Q: Can I take it self-paced, and will I get a certificate?<br/>
A: Yes, you can start anytime. Certificates require completing the final project and 3 peer reviews during a live cohort.

## About DataTalks.Club

<p align="center">
  <img width="40%" src="https://github.com/user-attachments/assets/1243a44a-84c8-458d-9439-aaf6f3a32d89" alt="DataTalks.Club">
</p>

<p align="center">
<a href="https://datatalks.club/">DataTalks.Club</a> is a global online community of data enthusiasts. It's a place to discuss data, learn, share knowledge, ask and answer questions, and support each other.
</p>

<p align="center">
<a href="https://datatalks.club/">Website</a> •
<a href="https://datatalks.club/slack.html">Join Slack Community</a> •
<a href="https://us19.campaign-archive.com/home/?u=0d7822ab98152f5afc118c176&id=97178021aa">Newsletter</a> •
<a href="http://lu.ma/dtc-events">Upcoming Events</a> •
<a href="https://www.youtube.com/@DataTalksClub/featured">YouTube</a> •
<a href="https://github.com/DataTalksClub">GitHub</a> •
<a href="https://www.linkedin.com/company/datatalks-club/">LinkedIn</a> •
<a href="https://x.com/DataTalksClub">X</a>
</p>

All the activity at DataTalks.Club mainly happens on [Slack](https://datatalks.club/slack.html). We post updates there and discuss different aspects of data, career questions, and more.

At DataTalks.Club, we organize online events, community activities, and free courses. You can learn more about what we do at [DataTalks.Club docs](https://datatalks.club/docs/general/).
