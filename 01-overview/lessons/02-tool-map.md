# The Tool Map

Video: TBA

## Agents

The role of an agent is to perform a task. To do that it uses tools:

- edit files
- execute bash commands
- search the web
- call an API
- and others

Everything in this lesson is an agent -
they differ in where they run, what tools they get, and how much they
are allowed to touch without asking you.

In the 2025 cohort this lesson was most of the module. We went through
products one by one, with install commands and links.

This year we will only briefly go over them. If you want to get more information
about them, check [2025 module 1](../../cohorts/2025/01-overview/).


## Main categories

There are five main categories:

- Chat assistants - you type, it answers, you copy the code out by hand
- Coding agents - work directly in your repo, in the terminal or
  in a desktop app
- Agentic IDEs - agent in your editor, with diffs you accept or reject
- Cloud agents - run in the cloud: you assign a task and review a pull request
- Project bootstrappers - start from a template instead of an
  empty folder, so you get a running app in minutes

### 1. Chat assistants

The general-purpose assistants, used in a browser:

- ChatGPT
- Claude
- Gemini

You type, it answers, you copy code out by hand. 
They have no access to your machine, so for coding they are not always convenient. Every time you need to make a change, you have to do a lot of copy-pasting. That is fine for a few files, but gets annoyning for bigger projects. 

Coding agents fix that, but chat assistants are still useful.

I use them every day for things related to coding:

- brainstorming - working a rough idea into a concrete one, usually by
  dictating rather than typing
- research - is there a library for this, what it does, and what the
  alternatives are
- checking what is already out there - whether the whole thing exists
  already, before I start building it
- saving the output - "save this to a md file" at the end, so we don't lose
  the result 

I also recommend chat when you are learning something new and you
actually care how it works. Copy-pasting slows you down, and it forces you to read what you are pasting.

If you learn about RAG, a coding agent can create the whole applicaiton a single prompt (we call it "one-shot" as a verb).
You end up with an application that is probably working fine, but you do
not understand how it works.

In a chat assistant you discuss the code as it appears and paste it in yourself,
so you learn more on the way.

We use a chat assistant in [lesson 3](03-specs.md) to produce the spec.

### 2. Coding agents

In the terminal:

- Claude Code
- Codex
- Gemini CLI
- GitHub Copilot CLI
- OpenCode
- Pi

You run them inside your code repository. They can read and edit files, run tests, perform web search. You no longer need to copy-paste.

I created the initial classification more than a year ago. Since then most coding agents have also grown a desktop app:

- Claude Cowork - Anthropic's desktop agent, works inside a folder you
  point it at
- ChatGPT Work - since July 2026 Codex and ChatGPT live in one desktop
  app
- ZCode - Z.ai's desktop agent
- OpenCode Desktop
- Antigravity (V2)

I use coding agents every day, mostly in terminal mode.

With coding agents, you have another problem. They can do anything on your computer, so you need to control what they can do and what they can access. 

Approving permissions is quite slow, so you can run them in the skip-permissions mode, but it's dangerous. In this case, you need to run them in an isolated enviroment where the blast radius is contained. 

I run them on a remote machine. If an agent wipes that machine I can recreate it in minutes. I wrote up how that is set up in [The System I Built for AWS Access
Without Keys](https://alexeyondata.substack.com/p/the-system-i-built-for-aws-access).

But I would suggest not to worry about these things right now. If you are setting an agent for the first time, here's a step-by-step
guide: [How to Set Up Your Coding
Agent](https://alexeyondata.substack.com/p/how-to-set-up-your-coding-agent-a).

You first pick up an agent, and then focus on doing one real task in it. Then gradually you add the rest - context files, permissions, slash commands, skills,
subagents, and a remote setup - one piece at a time.

### 3. Agentic IDEs

Roughly the same capability as a terminal agent, wrapped in an editor:

- Cursor
- Windsurf
- GitHub Copilot
- Zed
- Antigravity (V1)

The work is more interactive: you see diffs in the file and accept or
reject changes.

This is the most comfortable category for getting started, and for
staying close to the code.

I stopped using them because they slow me down. I noticed I was
fast-forward accepting changes anyway and rarely reviewing the diffs at
the end.

I treat my coding work now as PM and architect work, so I stay
on the high-level details rather than the implementation ones. For code
that matters I do a separate refactoring session once it already works.

### 4. Cloud agents

Agents need an environment to run in, and sometimes providing one is
inconvenient.

Most providers now host that environment for you:

- GitHub Copilot - create an issue and assign it to Copilot
- Claude Code on the web - connect a repo, submit a task, review the PR
- Codex cloud - the same shape, or tag `@codex` on a GitHub issue

We talked about it when discussing the disadvantages of coding agents. Here the  blast radius is limited to a restricted cloud environment. But it will not necesarily have the tooling you
need, and you have less flexibility in general.

I used GitHub Copilot this way a lot - that is the setup behind
[Shipping Features from my
Smartphone](https://alexeyondata.substack.com/p/shipping-features-from-a-tram-stop).

Eventually I moved to a remote machine running normal coding agents,
described in [The System I Built to Ship Code From a
Phone](https://alexeyondata.substack.com/p/the-system-i-built-to-ship-code-from).

### 5. Project bootstrappers

Coding agents start from an empty folder. But you can start from a template. 

That's exactly what project bootstrappers do. 

Some of them are:

- Lovable
- Bolt.new
- Replit
- Vercel v0
- Claude Design

One-shotting an app is much easier with a template. The coding agent is only building on top of it, so every app shares a tech stack you already
know how to run.

It is the fastest way to a first draft. These tools
also have their own design systems, so what comes out usually looks
better than a web app one-shotted by a plain coding agent.

However, they tend to get expensive with regular use. I
use them for a first version, export it, and continue with a coding
agent.

That is the flow in [How I Rebuilt My Website in 10 Minutes With
AI](https://alexeyondata.substack.com/p/how-i-rebuilt-my-website-in-10-minutes),
and we follow the same approach in [Module 2](../../02-end-to-end/).

## The harness

We already talked about agents. Harness is a piece of software that 
turns plain LLM calls into agents and adds many other capabilities on top:

- expose tools to the model
- execute the calls it asks
- feed the results back and run it until the task is done
- enforce permissions - what runs freely, what needs your approval
- manage context: what gets loaded, what gets compacted, what is
  dropped

The model makes the decisions, and the harness enables them.

The fastest way to understand what harness and agents are is build 
a coding agent yourself.

Last year we had a section about building your own agent. This year we will
focus on dev tools, but if you're interested, I have an updated verion of that material here: [Build a Coding Agent with Tools, Skills and
PydanticAI](https://aishippinglabs.com/workshops/coding-agent-v2).

In this workshop we start from a plain API call with no tools and end with a working agent
loop - five tools and a skills system. 

## Selecting the right tool

Which one do you need? It depends. 

In the end most of them do more or less the same thing. Pick one of:

- Codex
- Claude
- Antigravity
- Cursor
- GitHub Copilot

I mostly use Codex and Claude. I was a big fan of Copilot until the
June pricing change, which made it too expensive for how I work.

Codex
is probably the easiest to start with - the limits on the $20 plan are
generous.

Use a paid plan. You can run something like Antigravity for free, but
the free tiers are limited enough to be annoying: you get into the flow
and immediately hit a wall.

Then stay with it for the cohort. Every switch restarts the learning
curve, and none of the practice compounds.

Next: deciding what you want before anything gets built.

[← Introduction](01-intro.md) | [Specs Before Code →](03-specs.md)
