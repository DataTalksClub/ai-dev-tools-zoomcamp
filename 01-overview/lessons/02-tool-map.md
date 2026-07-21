# The Tool Map

Video: TBA

## Why this lesson is short

In the 2025 cohort, the tool tour was most of this module. We went
through products one by one, with install commands and links.

let's link the old content so people can read it if they want
let's cut the fluff. I did it here - do it in other places. define fluff based on my cuts and remove it

let's define what agent is. the task of the agent is to perform a task set by the user. the agent uses tools to do that. tools inclue - editing files, executing bash commands, performing web search. all the tools that we cover below are agents, but different ones.


## The five categories

### 1. Chat assistants

- ChatGPT
- Claude
- Gemini

You type, it answers, you copy code out by hand. This is still the best
place for thinking out loud: explaining an unfamiliar library, talking
through a design before committing to it, arguing about trade-offs,
drafting a spec.

Where it hurts is repo awareness. Every time you need to change,
you have to copy-paste back-and-forth. it's fine for a few files,
but becomes difficult
when you need to do more. coding agents fix this (we/ll talk about them later) but chat assistants are still quite useful and I use them regularly.

How I use it:

- dictation mode 
- brainstorming
- research
- checking what's already there
- "save to md file" at the end of the session

I also recommend to use it when you're learning about something new and you care about the implementation details and you want to learn. copy-pasting slows you down 
and forces to undestand better what you're doing. 

let's say you're learnign about RAG. coding agents can one-shot the entire thing (create a working application from a single prompt), but you will have very little idea how it works and you will need to read every sinble file to undestand it.
If you're in the chat application you can already discuss the code and you'll be forced to copy-paste it, so you'll learn more about the code this way.



### 2. Coding agents

Terminal coding agents

- Claude Code
- Codex
- Gemini CLI
- GitHub Copilot CLI
- OpenCode
- Pi (?)

These run in your terminal, inside a real repo. They read files themselves, edit several at once,
run your tests, and read the failures. The copy-pasting problem disappears. 

The cost is that something is now writing to your disk and running commands, so you need permission discipline: know what it can do without asking, and check
before you say yes to the rest. 

Or you need to run them in sandbox environments to make sure that the blast radius is minimal.

I creted this classification one year ago. Now most of the coding agents also have a proper desktop environment

- Claude Cowork
- Codex/ChatGPT Work
- OpenCode Desktop
- Z.AI coder (?)
- Antigravity (used to be Agentic IDE - now mo)

I use them every day. 
I mostly use them in the terminal mode, and they are running on a remote machine. 
If one of the agents wipes the machine, I can easily recreate it. 

More about it: substack AWS management.

### 3. Agentic IDEs 

Cursor, Windsurf, GitHub Copilot, Zed, Antigravity.

Roughly the same capability as a terminal agent, wrapped in an editor.

The work is more interactive: you can see the diffs in the file, and can accept
or reject code changes.

This is the most comfortable category for getting started with coding agents,
and being close to the code. 

I stopped using them because it slows me down. I noticed that often I just fast-forward accept the changes and at the end rarely review the diffs. 
I consider my coding work now more like a PM/Architect, so I focus on more high-level details instead of low-level implementation details. 

For important code, I later do separate refactoring sessions when the code already works. 

So I stopped using these agentic IDEs altogether.


### 4. Cloud and GitHub-native agents

for agents (both desktop and ides) you need environment to run them. 
sometimes it's inconvenient. lucikly many llm providers have cloud env 
where you can run your agents

- GitHub Copilot - create an issue and assign it to Copilot
- Claude Cloud ?
- Same for codex  (what's the name?)

benefits - you limit the blast radius (they can't cause much harm in the restricted cloud env) but also they don't necessarily have the tooling you need, and often you have less flexibilily

I used to use github copilot quite often (include my article about shiping from a tram stop) but eventually I created a flow where I use a remote machine with usual coding agents (see article about coding from phone)


### 5. Project bootstrappers

- Lovable
- Bolt.new
- Replit
- Vercel V0
- Claude Desing (?)

Coding agents start from scratch. Most applications can be started from a template.
When you have this template, doing one-shot apps becomes a lot easier, plus the apps created from these templates use the same tech stack, so you can always know how to run them locally.

that's the idea behind what I call "project bootstrappers". 

You describe what you want in a browser session and get a running app within minutes.
Typically this is the fastest way to create a first draft. 
Also these apps often have their own design systems, so the designs that these apps create are usually nicer than what you'd create when you single-shot an web application
using a usual coding agent. 

THe main downside is the cost-  they tend to get quite expensive with time. 
I usually use these tools to create a first version, then export it and continue working with it using a coding agent. 

I described the flow in my article how I redesigned my website. We will also follow the same appreoach in module 2.

## Harness

explain what harness is, what's the difference between plain llm calls
link the workshop from ai shipping labs about implementing our own agent

harness can do:

- tool calls
- permissions
- etc 

so it's things around the agents that make them usaful 

## Selecting the right tool 

Which tool do you need? The answer is "it depends". Notice that some tools are in all categories - like Claude. Codex and Copilot also appear in most of them. 

In the end, most of them do more or less the same. I'd recommend selecting one of them:

- Codex
- Claude
- Antigravity
- Cursor 
- Github Copilot 

I mostly use Codex and Claude. I was a big fan of Copilot until they changed their prices in June, and now it's too expensive to use it. Codex is probably the easiest to get started with as they have generous limits in the $20 plan. 

I also recommend using a paid plan. You can use tools Antigravity for free, but their free plans are quite limited and I find these limitations annoying. You get into the flow, and immediately hit the limits. 


## The fuller 2025 tour

If you want the longer version, the 2025 module is still in this repo:

- [cohorts/2025/01-overview/](../../cohorts/2025/01-overview/)

Read it for the categories and the shape of each one. Do not read it as
a product list. The specific tools named there have moved on, some of
the install commands no longer apply, and a couple of the products are
not the same thing they were. That is the whole reason this lesson
exists in its compressed form.



Next: how to use whichever tool you picked to get oriented in a codebase
you did not write.

[← Introduction](01-intro.md) | [Understanding an Unfamiliar Codebase →](03-understanding-codebase.md)
