# What other courses teach for AI-native development (July 2026)

**Date:** 2026-07-21
**Purpose:** Input for the 2026 redesign of Module 1 (AI-Native Developer Workflow).
**Method:** Automated multi-source research — 5 search angles, 24 sources
fetched, 120 claims extracted, 25 verified by 3-vote adversarial
verification (a claim needed 2 of 3 verifiers to refute it to be killed).
22 confirmed, 3 refuted.

> [!WARNING]
> This is a snapshot of a fast-moving field, and it is **not a census**.
> All landscape conclusions rest on six courses. See
> [Coverage gaps](#coverage-gaps) before treating anything here as
> settled. Re-check before the 2027 cohort.

## Sources examined

The six primary curricula that carry the findings:

| Course | Vintage | Notes |
|---|---|---|
| [Anthropic, "Claude Code in Action"](https://anthropic.skilljar.com/claude-code-in-action) | Current | Anthropic Academy / Skilljar. Single-vendor product course. |
| [GitHub GH-300 Copilot certification](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-300) | Effective 2026-08-07 | The only source with published domain weights. |
| [Vanderbilt, "Claude Code: Software Engineering with Generative AI Agents"](https://www.coursera.org/learn/claude-code) | ~mid-2025 build, still live | Coursera. Labelled Beginner. |
| [DeepLearning.AI × JetBrains, "Spec-Driven Development with Coding Agents"](https://www.deeplearning.ai/courses/spec-driven-development-with-coding-agents) | Announced ~2026-04-15 | Taught by Paul Everitt. [Files repo](https://github.com/https-deeplearning-ai/sc-spec-driven-development-files). |
| [Stanford CS146S, "The Modern Software Developer"](https://themodernsoftware.dev/) | Fall 2025 | No 2026 re-offering found. [Assignments repo](https://github.com/mihail911/modern-software-dev-assignments). |
| [TalTech ITS8090, "Agentic Software Development"](https://courses.taltech.akaver.com/agentic-software-development/lectures/intro) | Updated 2026-05-04 | 3 ECTS, 16 weeks, ~60 students, Andres Käver. |

Supporting primary sources: [agents.md](https://agents.md/),
[GitHub Spec Kit](https://github.com/github/spec-kit/blob/main/spec-driven.md),
[Kiro feature specs](https://kiro.dev/docs/specs/feature-specs/),
[Claude Code worktrees](https://code.claude.com/docs/en/worktrees) and
[agent teams](https://code.claude.com/docs/en/agent-teams) docs,
[OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/),
[Anthropic on sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing),
[METR uplift update (2026-02-24)](https://metr.org/blog/2026-02-24-uplift-update/).

## Headline finding

The field has converged on a spine that is **not** a tool taxonomy. It is
a *managed session*: steer → configure → automate → verify.

Anthropic uses these four verbs as literal top-level module headings.
Page tagline, verbatim:

> Run long, hands-off Claude Code sessions you can trust: steer,
> configure, automate, and verify

Target audience, verbatim: "Developers who already use Claude Code for
single prompts and want to move to longer, less supervised, team-wide
workflows."

**Important caveat carried from verification:** Anthropic omits tool
comparison because it is a single-vendor product course, **not** because
comparison is obsolete. Do not cite it as evidence for cutting a
comparison unit. Stanford keeps IDE (Week 3) and terminal (Week 5) as
separate weeks with separate assignments — comparison survives as
sub-material, not as an organizing spine.

## Confirmed findings

### 1. Session steering is taught as named mechanics (high confidence)

Not a generic "AI development loop". Anthropic's "Steer the Work" module
objective, verbatim:

> scope work with plan mode, direct compaction so summaries keep what
> matters, use the rewind menu to course-correct, and choose between
> hands-on steering and autonomous goal and loop runs

Lesson title: "Steering Long Sessions".

> [!NOTE]
> The Coursera mirror of this course is an **older cut** (modules: What
> is Claude Code? / Getting Hands On / Hooks and the SDK / Wrapping Up)
> that covers plan mode but not rewind or compaction-as-steering. Cite
> the Skilljar version. Anthropic never calls the four verbs a "loop" —
> they are four sequential curriculum sections.

### 2. Context engineering is now a layered system (high confidence)

"Write a CLAUDE.md" is no longer the lesson anywhere. Every current
curriculum teaches multiple layers.

Anthropic "Configure Claude" objective, verbatim:

> write a lean CLAUDE.md Claude actually follows, package repeated
> procedures as skills, pick the right permission mode for each job, and
> enforce the non-negotiable rules with hooks

Lessons: "A CLAUDE.md That Follows", "Verification Skills", "Permission
Modes", "Hooks".

GH-300, verbatim: "Utilize Spaces, Spark, Pull Request summaries, and
customizable review standards via instructions files" and "include prompt
file reuse for consistent responses".

Vanderbilt Module 3 "Building Process & Context in Claude Code": videos
"Global Persistent Context: CLAUDE.md", "Reusable Targeted Context &
Process: Claude Code Commands", "In-Context Learning: Teaching with
Examples".

### 3. AGENTS.md is an ecosystem fact, not a curriculum fact (medium confidence)

**Zero verified curricula teach `AGENTS.md` as a cross-vendor standard.**

- Full read of GH-300's skills-measured list (~1,076 words, all 6
  domains): the strings `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
  `copilot-instructions.md` appear nowhere. The "prompt engineering and
  context crafting" domain names no file format at all.
- Case-insensitive grep of the entire Stanford CS146S bundle (204,922
  bytes, all 10 weeks) for `AGENTS.md` / `CLAUDE.md`: **zero hits**.
- Vanderbilt teaches vendor-specific `CLAUDE.md`.
- DeepLearning.AI uses "constitution" files instead.

Meanwhile the *products* support it: GitHub Changelog 2025-08-28,
"Copilot coding agent now supports AGENTS.md custom instructions"; GitHub
Docs list "a single CLAUDE.md or GEMINI.md file stored in the root of the
repository".

**Reading:** certifications lag the product. `AGENTS.md` is a genuine
ecosystem convention that no examined curriculum has caught up to.

**Caveat:** this is an argument from absence in published objectives, and
Microsoft warns the bullets "are intended to illustrate how we are
assessing that skill".

**Implication for us:** teaching `AGENTS.md` is defensible and probably
correct, but frame it as *the portable convention* rather than *what
everyone teaches*.

### 4. Spec-driven development is a standalone mainstream unit (high confidence)

The single biggest gap against our existing outline. The generalizable
pattern: a persistent project **constitution** plus **per-feature specs**,
driving a repeatable **plan → implement → validate** loop with a mandatory
validation gate. Explicitly positioned as the disciplined alternative to
vibe coding.

DeepLearning.AI's 15+ lesson arc: Why SDD → Workflow overview → Creating
the constitution → Feature specification → Feature implementation →
Feature validation → Project replanning → Second feature phase → MVP →
Legacy support → Build your own workflow → Agent replaceability → graded
quiz.

Verbatim outcomes:

> Apply a repeatable plan-implement-verify workflow to fresh and legacy
> codebases

> Understand why detailed specs produce better, more maintainable
> software than vibe coding

> preserve context across agent sessions, improve intent fidelity, and
> reduce cognitive debt

The official repo confirms the two tiers as shipped artifacts: Video06
"Constitution in place (`specs/mission.md`, `tech-stack.md`,
`roadmap.md`)", Video07 "Constitution + Phase 1 feature spec (`plan.md`,
`requirements.md`, `validation.md`)".

TalTech independently devotes four consecutive lectures to it: "22 - Spec
Driven Development", "23 - OpenSpec", "24 - Spec Kit", "25 - BMAD".

> [!IMPORTANT]
> The three-file mission/tech-stack/roadmap split is **course-specific**.
> GitHub Spec Kit uses a single `constitution.md`. Teach the pattern, not
> the filenames.

### 5. Verification has replaced diff-reading (high confidence)

The biggest qualitative shift away from "human reviews the diff". Three
distinct teachable practices:

**(a) Rubric-based self-critique.** Vanderbilt, verbatim: "Teach Claude
Code to critique its own code using contextual rubrics that catch bugs
before you ever see them."

**(b) Best-of-N.** Vanderbilt, verbatim: "Use the 'Best of N' pattern with
Claude Code to generate 3-5 versions of every feature and cherry-pick the
best parts." Lesson: "The Best of N Pattern: Leverage AI Labor Cost
Advantages".

**(c) Post-hoc verification of unsupervised runs.** Anthropic Module 4
"Verify and Share" includes the lesson "Trust It: Verifying Unsupervised
Runs". Module 2 includes "Verification Skills" — verification packaged as
a reusable *artifact*, not an ad-hoc human read.

DeepLearning.AI makes "Feature Validation" a mandatory named step of every
feature cycle.

**Caveat:** "going beyond line-by-line review" is the analyst's gloss, not
course wording.

### 6. Parallel agents are beginner-level content (high confidence)

Vanderbilt Module 4 "Version Control & Parallel Development with Claude
Code": readings "Allowing Claude Code to Work in Parallel with Git
Worktrees", "Claude Subagents & Tasks", "Parallel Feature Development with
Subagents, Tasks, and Git Worktrees". Course description: learners
"orchestrate Claude Code working concurrently across multiple git
branches, with parallel AI agents developing different features
simultaneously and automatically integrating their work." Coursera labels
the course **Beginner**.

GH-300, verbatim: "manage Agent Sessions and delegate tasks to Sub-Agents
for optimized context usage".

> [!NOTE]
> **Depth caveat.** The Vanderbilt module is ~36 minutes of a ~5-hour
> course, 30 of which are readings. GH-300's subagent content is one
> bullet in one sub-objective. Presence is well evidenced; depth is not.

### 7. Automation outside the interactive session is its own module (high confidence)

Anthropic Module 3 "Automate Repeat Work", lessons "Routines and Headless"
and "GitHub Actions and Code Review". Body text: "schedule prompts as
routines on Anthropic infrastructure", "drop to headless mode when a job
needs your own pipeline", "wire Claude into pull requests with managed
code review and the GitHub action". Claude Code Routines shipped in
research preview 2026-04-14.

GH-300 has a named subsection "Use GitHub Copilot CLI" sitting as a
sibling of "Use GitHub Copilot in the IDE" — present since the January
2026 revision, so stable rather than preview.

### 8. Agent security has a dedicated week at both universities (high confidence)

Entirely absent from our Module 1 outline.

Stanford CS146S Week 6 "AI Testing and Security": topics "Secure vibe
coding", "History of vulnerability detection", "AI-generated test suites".
Readings include "Copilot Remote Code Execution via Prompt Injection"
(embracethered.com), "Finding Vulnerabilities in Modern Web Apps Using
Claude Code and OpenAI Codex" (semgrep.dev), "Agentic AI Threats" (Unit
42), OWASP Top Ten, "Context Rot: Understanding Degradation in AI Context
Windows" (Chroma). Graded assignment: "Scan and Fix Vulnerabilities with
Semgrep" — run Semgrep on a FastAPI/JS app, triage and remediate ≥3
issues. Guest: Isaac Evans, CEO of Semgrep.

TalTech "53 - Security and Safety" covers the lethal trifecta (private
data + attacker-controlled content + external comms), direct and indirect
prompt injection, RAG and memory poisoning, OWASP LLM Top 10, capability
scoping, human-in-the-loop authorization gates, sandboxing, and six
MCP-specific attack classes including tool shadowing and confused deputy.

### 9. The "agent manager" framing is explicit (high confidence)

Stanford Week 4 "Coding Agent Patterns", topics exactly two: "Managing
agent autonomy levels", "Human-agent collaboration patterns". The Monday
lecture is literally titled "How to be an agent manager". Friday guest
lecture by Boris Cherny, creator of Claude Code.

Vanderbilt's parallel framing: "orchestrate Claude Code like a tech lead
managing multiple senior developers" / "treating AI as scalable
development labor".

### 10. MCP is taught as hands-on build work (high confidence)

Stanford Week 3 graded assignment "Build a Custom MCP Server": 90-point
rubric, wrap a real external API, 2+ MCP tools, STDIO or HTTP transport,
error handling and rate limits, +5 extra credit for a deployed remote HTTP
server, +5 for OAuth2/API-key auth with audience validation.

TalTech has "27 - MCP" plus "28 - Skills". GH-300 names MCP in the
features domain.

*(Relevant to our Module 3, not Module 1.)*

### 11. Governance outweighs prompt engineering (medium confidence)

GH-300 domain weights, verbatim, "Skills measured as of August 7, 2026":

| Domain | Weight |
|---|---|
| Use GitHub Copilot responsibly | 15–20% |
| Use GitHub Copilot features | 25–30% |
| Understand GitHub Copilot data and architecture | 10–15% |
| Apply prompt engineering and context crafting | 10–15% |
| Improve developer productivity with GitHub Copilot | 10–15% |
| Configure privacy, content exclusions, and safeguards | 10–15% |

Three qualifications:

1. 15–20% + 10–15% = 25–35%, so say "a quarter to a third", not "a third".
2. The published list contains a genuine Microsoft **duplication error**
   ("Use GitHub Copilot features" and "GitHub Copilot features" both at
   25–30%), so weights sum to 105–135%. De-duplicate before doing share
   arithmetic.
3. Calling this "human-in-the-loop verification" overstates it — only one
   of five bullets in the Responsible domain is about validating output;
   the rest is GenAI ethics/harms, and the privacy domain is largely admin
   configuration.

The load-bearing comparison — responsible use alone exceeds prompt
engineering — holds under any reading.

### 12. Evals as "the spec for non-deterministic systems" (medium confidence)

TalTech lectures "51 - Errors, Determinism, Observability", "52 -
Evaluation and Testing", "53 - Security and Safety", "54 - Scaling Agents:
Cost and Multi-Agent Coordination".

Lecture 52 covers five core metrics (task completion, tool accuracy, cost,
latency, stability), seven eval methodologies (programmatic checks, golden
datasets, LLM-as-judge), the Inspect framework with worked examples, CI
integration, multi-agent eval. Verbatim premise:

> Evaluations are the spec for non-deterministic systems. Unit tests work
> because f(2) == 4 every time. An LLM-driven loop has no such guarantee.

**Confidence is medium because this is n=1** — one Estonian-language MSc
elective with ~60 students. It is an existence proof from a credible
institution, not an industry standard.

### 13. Benchmarks are essentially untaught (medium confidence)

Grep over the full 204,922-byte Stanford bundle for `swe.?bench`,
`terminal.?bench`, `benchmark`, `eval[su]`, `worktree`, `sub.?agent`,
`parallel agent`, `token`, `cost`: **zero hits**. No other verified
syllabus names them. TalTech teaches locally-owned Inspect-based eval
suites, explicitly choosing Inspect over Braintrust ("eval suites you
own"), not public leaderboards.

**Implication:** benchmarks are *tool-selection literacy* (how to read a
vendor claim), not a skill to practice. A 10-minute segment at most.

## Refuted claims

These were killed during verification. **Do not resurrect them.**

| Claim | Vote |
|---|---|
| Vanderbilt's syllabus has no MCP/hooks/plan-mode coverage | 0–3 |
| SDD replanning, legacy-codebase support, skills-packaging and "agent replaceability" are novel to 2026 | 1–2 |
| Cost management + multi-agent coordination are confirmed standard 2026 curriculum items | 0–3 |

The third matters most: it was over-generalized from a single lecture
title. Do not build a lesson on the premise that cost budgeting is
standard taught content.

## Caveats

### Vintage divergence

The six sources span very different vintages, and this changes how to read
their gaps. TalTech (updated 2026-05-04) and DeepLearning.AI (~2026-04-15)
are genuinely mid-2026. Anthropic's Skilljar course and GH-300 are current.
Vanderbilt is a ~mid-2025 build, still live, lightly re-edited. **Stanford
is a Fall 2025 snapshot** — its absences (no evals, no benchmarks, no
worktrees, no AGENTS.md, no Spec Kit) are partly a late-2025 artifact and
must **not** be read as proof those topics are absent from 2026 curricula.

### Platform divergence

Anthropic runs two differently-structured versions of "Claude Code in
Action" simultaneously. Claims about the four-stage spine are **false** of
the Coursera cut.

### Depth vs. presence

Several "a full module is devoted to X" findings overstate instructional
weight. Stanford's Week 7 code-review content is roughly one lecture +
assignment + guest, not the whole week; weekly assignments are
collectively only 15% of the grade.

### Coverage gaps

**No verified primary evidence** was gathered for: Udemy, Maven, Frontend
Masters, Scrimba, Pluralsight, OpenAI's or Google's official coding-agent
courses, or open-source curricula such as `microsoft/ai-agents-for-beginners`.
Absence of evidence is not evidence of absence — the landscape claims here
are drawn from **six courses, not a census**.

### Factual corrections applied during verification

- Stanford's graded "Build a Custom MCP Server" is **Week 3**, not Week 2
  (Week 2's is "First Steps in the AI IDE").
- The CS146S site misspells Boris Cherny as "Cherney".
- GH-300's published domain list contains a Microsoft duplication error.

## Open questions

1. What do the unsampled platform curricula teach (Udemy, Maven, Frontend
   Masters, Scrimba, Pluralsight, OpenAI, Google,
   `microsoft/ai-agents-for-beginners`)? The SDD-is-mainstream and
   evals-are-taught findings would be strengthened or weakened by that
   sample.
2. Is `AGENTS.md` actually converging as a cross-vendor standard, given
   that zero curricula teach it while GitHub, Anthropic and Google all
   ship product support? This determines whether we teach it as *the*
   default portable convention or as *an emerging* one.
3. Does Stanford CS146S have an Autumn 2026 re-offering? That diff would
   be the cleanest signal of what changed in university curricula between
   late 2025 and late 2026.
4. How are courses actually teaching token/cost budgeting and multi-agent
   economics? The one claim here was refuted for over-generalizing, so the
   concrete pedagogy remains unverified despite being obviously relevant
   to an "agent manager" framing.
5. What is the real pedagogical status of coding-agent benchmarks? The
   evidence is a negative grep on one 2025 syllabus plus absence
   elsewhere — enough to say they are not taught as a skill, not enough to
   say whether 2026 courses use them for tool-selection literacy.

## Implications for our Module 1

Ranked by how much they change the existing plan.

1. **Tool comparison stops being the spine.** Collapse to a single unit
   that points at the [2025 materials](../cohorts/2025/01-overview/) —
   "ignore the tool names, keep the categories" — plus choosing a tool and
   committing to it for the cohort.
2. **Spec-driven development becomes the backbone.** Constitution +
   per-feature spec, plan → implement → validate with a validation gate.
   Watch the boundary with Module 2, which already opens with a product
   spec.
3. **Context engineering expands from one file to a layered system.**
   `AGENTS.md` (with `CLAUDE.md` importing it via `@AGENTS.md`) plus
   reusable commands/skills, permission modes, and hooks.
4. **"Review the AI diff" becomes verification.** Rubrics, self-critique,
   validation gates, Best-of-N, and verifying unsupervised runs.
5. **Session steering gets named mechanics** — plan mode, compaction,
   rewind, supervised vs. autonomous — instead of a generic loop diagram.
6. **Decide on a security primer.** Two universities give it a full week;
   we have a whole Module 4. Options: a short prompt-injection and
   permission-scoping primer in Module 1, or defer entirely and say so.
7. **Benchmarks: ~10 minutes**, framed as reading vendor claims.

## Follow-up: "loop engineering" and "graph engineering"

Two terms proposed for the module that the main research did not surface
at all. Researched separately on 2026-07-21. **Neither is an established
term.** They differ sharply in how much real practice sits underneath.

### Loop engineering — real practice, unstable name (~6-7 weeks old)

Emerged early June 2026. Timeline of primary sources:

| Date | Source | Type |
|---|---|---|
| ~early June 2026 | Boris Cherny (leads Claude Code at Anthropic), X post | Origin spark |
| 2026-06-07 | [Addy Osmani, "Loop Engineering"](https://addyosmani.com/blog/loop-engineering/) | Best single primary source |
| 2026-06-09 | [Cobus Greyling essay](https://cobusgreyling.substack.com/p/loop-engineering) + [repo](https://github.com/cobusgreyling/loop-engineering) (8.9k stars) | Practitioner + tooling |
| 2026-06-23 | [Caspar Bannink, Towards AI](https://pub.towardsai.net/loop-engineering-is-the-new-agentic-engineering-180a59d748bf) | Practitioner |
| **2026-06-30** | [Anthropic, "Getting started with loops"](https://claude.com/blog/getting-started-with-loops) | **First-party vendor doc** |
| July 2026 | [aipatternbook.com/loop-engineering](https://aipatternbook.com/loop-engineering) | Cleanest technical definition |
| July 2026 | IBM glossary, SEO content mills | Buzzword-stage pickup |

**What it means.** Designing the outer control system that repeatedly
invokes an agent over time — not any single prompt or single run. Five
recurring components:

1. **Discovery** — how the system decides what to do next (failing tests,
   issue queue, CI signal, schedule)
2. **Isolated handoff** — packaging a task into a sandbox (git worktrees,
   ephemeral branches)
3. **Independent verification** — checking the result with something the
   agent didn't write (tests, linters, separate evaluator, CI)
4. **State persistence** — durable progress across iterations (`STATE.md`,
   PR history, issue tracker)
5. **Stop condition** — goal met, budget cap, iteration limit, human gate

Positioned by every source that addresses it as a **successor layer, not
a replacement**: prompt engineering → context engineering → harness
engineering → loop engineering. Context engineering governs what goes into
a single call; loop engineering governs how often, on what, and under what
verification the agent gets called at all.

Anthropic productized it: `/goal`, `/loop`, `/schedule` in Claude Code,
formalized as four loop types (turn-based, goal-based, time-based,
proactive).

**Status:** not settled. At least four competing framings exist. Six weeks
from coinage to SEO content mills is textbook buzzword propagation. But
the underlying practice is genuinely built and used, so the term names
something real.

**Best line to teach from** (aipatternbook.com):

> the autonomy ceiling is set by verification reach

**Sourcing caveat from the researching agent:** most pages were read
through an LLM summarizer, which risks paraphrase drift. The Cherny quote
in particular ("I don't prompt Claude anymore… My job is to write loops")
should be checked against the original before being quoted verbatim
anywhere student-facing.

### Graph engineering — do not build a lesson on this

**Three days old.** Originates from a single Peter Steinberger (@steipete)
X post, **2026-07-18**: *"Are we still talking loops or did we shift to
graphs yet?"* (575K views), itself a sequel to his June "loop engineering"
post. No vendor doc, no syllabus, no talk uses it as a stable concept —
only SEO blogs written within 72 hours
([explainx.ai](https://www.explainx.ai/blog/graph-engineering-ai-agents-multi-agent-organizations-2026),
[aibuilderclub.com](https://www.aibuilderclub.com/blog/graph-engineering-guide-2026),
both course-marketing sites).

The term is contested by the people using it:

- **Harrison Chase (creator of LangGraph)**: "so i didn't really know what
  graph engineering is, and i still don't really… but it's basically just
  langgraph?"
- **Karan Singh**: "Sub-agents with a defined purpose is a Graph. But yeah
  lets confuse everyone and call it a net new thing."
- **David K (creator of XState)**: "First it was loops. Now it's graphs.
  Next month it'll be something else... we're constantly rediscovering
  decades-old software engineering patterns."

**Dominant reading:** orchestrating multiple agents as a DAG, LangGraph
style — nodes are specialized agents, edges are routing. The
codebase-as-graph reading (call graphs, dependency graphs, repo maps)
**did not surface at all** under this label, despite being a real practice
with real tools (Aider's repo-map, Sourcegraph, CodeQL, Joern).

> [!WARNING]
> **Name collision.** "Graph engineering" has an established, unrelated
> meaning in data engineering and network analysis — graph databases,
> schemas, Cypher, graph algorithms at scale. That older sense is stable
> and real. The AI-coding sense is a brand-new colloquialism reusing the
> same two words. A DeepLearning.AI knowledge-graph course by Neo4j's
> Andreas Kollegger got pulled into the same X debate purely by timing
> coincidence — it does not use the term.

**Recommendation:** do not name a lesson after it. The course records now
and runs from 2026-08-31; a lesson named after a three-day-old tweet ages
badly within weeks. Teach the durable substance instead — parallel agents
on worktrees and subagents, which the main research independently
confirmed as *beginner-level mainstream* content (Vanderbilt module,
GH-300 objective). The buzzword is worth one honest aside as a case study
in how fast this vocabulary churns.
