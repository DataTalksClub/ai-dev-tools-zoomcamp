# Judgment and Wrap-up

Video: TBA

Everything in this module so far has been a technique you can follow.
Read a codebase this way. Write the spec before the code. Put durable
facts in `AGENTS.md`. 

## The three-way decision

I don't undsetand where it's coming from - in summary we only talk about things we mentioned previous 
let's rewokr the whole spec-driven development thing

You make one decision over and over during a working day, usually
without noticing it. A piece of work arrives and you choose:

1. **Delegate it** - hand it to the agent
2. **Inspect it yourself** - read every line before it lands
3. **Simplify it** - the task is wrong as stated, so cut it down

Most people only think about the first two, and treat it as a question
about the model's capability. It mostly isn't. It is a question about
you: what you can check, and what you will have to answer for later.

### Delegate when the work is well-specified, verifiable and reversible

- **Well-specified**: you could write down what "done" looks like in
  three lines. If you can't, that is a specs problem, not an agent
  problem. Go back to [lesson 4](03-specs.md).
- **Verifiable**: something other than the agent's own opinion can tell
  you it worked. A test, a type checker, a build, the app running in
  front of you.
- **Reversible**: if it is wrong, `git checkout` undoes it and nothing
  else was touched. Uncommitted work in a clean tree is reversible. A
  migration that already ran against a real database is not.

All three true, delegate it and don't feel bad about it. That covers
most of the work in most repos.

### Inspect yourself in two situations

**When you will have to defend it.** A reviewer, a colleague six
months from now, an incident channel at 2am. Inspecting doesn't mean
typing it yourself - the agent can still write the code. It means the
result passes through your head before it passes into the repo.

**When you don't yet understand the problem well enough to check the
answer.** This is the one people get backwards. The instinct is: I
don't know this area, so let AI handle it. But that is exactly the
situation where every answer looks equally plausible and you have no
way to tell a good one from a confident one.

Out of your depth is a reason to slow down, not to speed up. Use the
agent to get to the point where you can judge: ask for explanations,
ask it to point at the files it is basing them on, take one small step
and confirm it before the next.

### Simplify when two attempts have failed

Here is a rule I actually use: **after two failed attempts, change the
task, not the prompt.**

The third rephrasing almost never works. A task an agent keeps failing
is usually too big or too vague rather than too hard, so the failure is
information about the task. Instead of attempt number three:

- Split it into three tasks and do the first one
- Name the specific file and function instead of describing the
  outcome
- Write the failing test first, then ask for the code that passes it
- Do the confusing part by hand, delegate the rest
- Start a fresh session, because the old one is now full of wrong turns
  ([lesson 6](07-implementing-a-task.md))

All of these are the same move: make the unit of work smaller and more
concrete. That is nearly always the fix.

## You can delegate the typing, not the responsibility

"The AI wrote it" is not a defence, any more than "I copied it off
Stack Overflow" ever was. The code is in your repo with your name on
the commit.

The test I keep coming back to:

> If you can't explain a change in review, you are not finished with
> it, however well it works.

Not explain in detail, line by line. Explain: what it does, why it
does it that way, and what would break if it were wrong. That is a low
bar and a surprising amount of AI-assisted work fails it.

This is why [lesson 1](01-intro.md) opened with three questions - what
did I ask for, what actually changed, how do I know it works. They are
the same test in three pieces.

## Understanding debt

Code you did not read and cannot explain accumulates like technical
debt: quietly, with no visible symptom, and it comes due at the worst
moment - something breaks and you are opening a file you have never
seen in a system you supposedly built.

This is not an argument against delegating. It is an argument for
knowing which parts you chose not to read, and why. There is a real
difference between these two:

- "I skimmed the CSS and the boilerplate. I know I skimmed it. If it
  breaks I'll read it then."
- "I don't know how any of the authentication works, and I shipped it."

The first is a reasonable trade. The second is a problem you have not
noticed yet.

So keep it visible: the parts you skip should be the parts where being
wrong is cheap. If the core of your system is a black box to you, pay
it down now rather than during an incident - ask for a walkthrough,
read the files, write a test that proves you understood it correctly.

The cheapest payment is the diff. Reading changes as they land takes a
minute. Catching up on six weeks of unread code takes a weekend.

## When to slow down

Some areas get inspected regardless of how well-specified the task
looked:

- Authentication and authorization
- Secrets, tokens, credentials, anything near `.env`
- Payments and billing
- Anything that deletes or migrates data
- CI configuration and workflow files
- Deployment, infrastructure, access permissions
- Anything else that is hard or slow to reverse

The common thread is that the cost of being wrong has nothing to do
with the size of the diff. A one-line change to a permission check is
one line. It is also the whole security model of your application.

In these areas: ask for a plan before edits, keep changes small, read
every line, and don't run unattended loops over them. That last point
is [lesson 8](09-loop-engineering.md)'s rule from the other side - the
autonomy ceiling is set by verification reach, and here yours is
short.

## The arc of the module

Wrapping up. The working practices, in the order real work happens:

```text
3  understand the code       where am I
4  specify the change        what am I asking for
5  give durable context      what does the agent know before it starts
6  steer the session         what do I do while it runs
7  verify the result         how do I know it works
```

Then the vocabulary, for words you'll meet outside this course without
a definition attached: [loop engineering](09-loop-engineering.md), one
agent iterating against a check until a stop condition, and [graph
engineering](10-graph-engineering.md), several agents with defined
roles handing work between them.

## What you should have now

Two things.

```text
AGENTS.md    what your project is, how to run it, how to test it,
             what an agent should not do
CLAUDE.md    one line: @AGENTS.md
```

And one tool you committed to for the cohort, which you are now a few
weeks less of a beginner with than you were in
[lesson 2](02-tool-map.md).

## The homework

[Build a Django TODO app](../../cohorts/2026/01-overview/homework.md)
with the tool you picked.

You do not need to know Django. That is the point of the exercise: it
puts you in the situation from earlier in this lesson, where you can't
check an answer by recognising it, so you have to check it the other
ways. Run it. Make it tested. Ask the agent to explain the pieces you
don't recognise, and read the files it points at.

Finish it, and be able to explain what each part of the app does.

## What comes next

[Module 2](../../02-end-to-end/) builds and ships a full-stack
application end to end, with these habits applied to something bigger
than a single-screen app.

[Module 3](../../03-mcp/) goes deep on agent capabilities - MCP,
skills, hooks, subagents, plugins, custom agents. That is the
machinery we only named in lessons 5, 8 and 9, and where the setup
instructions live.

## The durable point

Some of the tools we named in this module will be different by the end
of this course, and a few will not exist. That is not a problem with
the module. It is the reason it is shaped this way.

What transfers is smaller and duller than any product:

- Specify before building
- Give durable context instead of repeating yourself
- Verify with something independent of the thing you are checking
- Keep the judgment, delegate the typing

That works with a coding agent, with a colleague, with whatever ships
next year. Everything else is an interface over it.

See you in Module 2.

[← Graph Engineering](10-graph-engineering.md) | [Back to module →](../)
