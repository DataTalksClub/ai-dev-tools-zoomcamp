# Tests and Verification

Video: TBA

Everything up to this point has been about getting an agent to do more
of the work: briefing it well, giving it a spec, steering it when it
drifts. This lesson is about the other half. How do you *know* the
work is right?

Verification is what makes delegation safe. Not the model being good,
not the code looking reasonable, not the agent sounding confident.
Verification. It is the difference between AI-assisted work you can
defend in a review and work you merely hope is fine.

## The central principle

State it plainly, because everything else follows from it:

> An agent that writes the code and then judges whether the code is
> correct is grading its own homework.

By the time it finishes, it has spent its entire context convincing
itself that its approach was the right one. Asking "is this correct?"
at the end asks it to disagree with itself, and it will not. You get
"yes, this correctly handles the edge case", where the edge case is
the one it thought of, handled the way it decided to handle it.

So the rule:

> Real verification comes from somewhere the work did not.

A test the agent has to pass. A type checker it cannot argue with. A
running app that either draws the screen or does not. A fresh session
with no memory of the last two hours. A human. Everything below is a
way of arranging for that.

## What your project can check without a human

Before you can delegate anything, you need to know what your project
can already tell you on its own. Most people have never made this
list, and it is genuinely useful information about a codebase.

| Check | What it catches |
|---|---|
| Tests | Behaviour that changed when it shouldn't have |
| Type checker | Wrong shapes, wrong arguments, wrong returns |
| Linter / formatter | Style drift, unused code, obvious mistakes |
| Build / compile | Code that does not even hold together |
| Running the app | Whether the thing works at all |
| CI | All of the above, on someone else's machine |

Go and inventory your own project. Write down the exact command for
each one, and how long it takes. Something like:

```text
make test        pytest, 12s, 84 tests
make typecheck   mypy, 6s
make lint        ruff, 2s
make run         starts the dev server on :8000
CI               runs all of the above on push
```

Two things come out of this. First, those commands belong in
`AGENTS.md`, so the agent runs them itself instead of asking you or
guessing. That is part of the module deliverable from
[lesson 5](05-context-engineering.md). Second, the length of that list
is a measurement, and we come back to what it measures at the end of
this lesson.

If the list is empty, that is the finding. It means every check on
this project is you, reading.

## Tests as the guardrail

Tests are what let you delegate without reading every line. A change
that keeps a good suite green is a change you can accept without
holding the whole implementation in your head.

Four practical notes.

**Make the agent run them, not just write them.** Writing a test is
generating text. Running it is an observation. An agent that has run
the suite and pasted the output is telling you something; an agent
that says "this should pass" is not. Ask for the output.

**Be suspicious of tests written in the same pass as the code.** If
the same agent, in the same context, wrote both the implementation and
the test, they can encode the same misunderstanding. The test passes
because it asserts exactly what the code does, which is not the same
as asserting what the code should do. This is the same problem as
before, wearing a test suite as a disguise.

Two ways around it. Write the acceptance criteria yourself, before
implementation, as you did in [lesson 4](04-specs.md) - then the test
is checking your intent, not the agent's. Or have a separate pass, in
a fresh context, write tests against the spec rather than against the
code.

**A test that has never failed has not proven anything.** It might be
asserting something trivially true. It might not be running at all.
Break the code on purpose and watch the test go red. That takes
fifteen seconds and it is the only way to know the test is wired up
to the behaviour it claims to cover.

**Watch for tests that get deleted or weakened.** When an agent is
told "make the tests pass", deleting the failing test is a valid
solution to the instruction it was given. So is loosening an
assertion, or adding a skip marker. Check the diff for tests removed,
not just tests added.

## Reading the diff

You still have to read the diff. But a general skim is not much use -
you will nod along at plausible-looking code. Read it looking for
specific things:

- **Changes you did not ask for.** The most common one. It fixed your
  bug and also renamed three things and reorganized a module.
- **Files touched that had no reason to be touched.** Ask why each
  file in the diff is there. If the answer is not obvious, ask the
  agent.
- **New dependencies.** A package added to solve something small is a
  permanent cost. Question every one.
- **Changes to auth, permissions or anything security-adjacent.**
  Read these line by line, always.
- **Secrets, keys, tokens, `.env` files.** Committed by accident,
  hardcoded "temporarily", printed in a log line.
- **CI and deployment config.** A quiet edit to a workflow file or a
  Dockerfile has a much longer blast radius than a code change.
- **Deleted or skipped tests.** As above.
- **Code more elaborate than the problem needed.** An abstraction
  layer, a config option, a plugin system, for a task that needed
  twenty lines. Complexity you did not ask for is complexity nobody
  is going to maintain.

A smaller diff is easier to read, which is another argument for the
small-steps habit from [lesson 6](06-steering-a-session.md). If you
cannot review a change, you have not really delegated it, you have
just stopped looking.

## Getting a second opinion

The cheapest way to get verification from outside the work is to run
the review in a context that did not do the work.

A fresh session, given the diff and the original spec, has none of the
original's investment in the approach. It did not spend an hour
deciding that this was the right design, so it is free to say the
design is wrong. A different tool entirely works even better: it will
have different blind spots too.

This is not a tooling trick, it is the principle applied. The
mechanism is the same whether it is a separate session, a subagent, or
a colleague.

When I built a small team of agents with fixed roles, the thing that
made it work was separating the role that writes code from the role
that checks it, with the checker running in its own context:
[I Built an AI Agent Team for Software Development](https://alexeyondata.substack.com/p/i-built-an-ai-agent-team-for-software).
[Lesson 9](09-graph-engineering.md) goes into that system properly.

## What cannot be checked automatically

Automatic checks tell you the code does what the code says. They
cannot tell you:

- **Whether it is what the user actually wanted.** A feature can pass
  every test and still solve the wrong problem. This is why specs come
  before code, and why you re-read the spec at the end.
- **Whether the design will survive the next change.** Tests pass on
  code that will be miserable to extend in three weeks. No linter
  reports that.
- **Whether it is appropriate.** Whether this feature should exist,
  whether the tradeoff is acceptable, whether the thing is worth
  doing at all.

These stay yours. They are the part of the job that does not get
delegated, and [lesson 10](10-wrap-up.md) is about them.

## The idea to take with you

Put the pieces together and you get a rule that decides how you work:

> You can delegate exactly as far as you can verify.

Or, more compactly: **the autonomy ceiling is set by verification
reach.**

A project with a fast, trustworthy test suite, a type checker and
green CI can support a lot of autonomy. You can let an agent work
through a queue of tasks, because when it is wrong, something says so
without you. A project with no tests cannot support that, no matter
how good the agent is, because nothing in the system is capable of
telling it that it went wrong.

That is why the inventory you made earlier matters. It is not
housekeeping. It is a measurement of how much you can safely hand
over, and it is the thing to improve if you want to hand over more.

Next: what happens when you take that ceiling seriously and design
the loop the agent runs in.

[← Steering a Session](06-steering-a-session.md) | [Loop Engineering →](08-loop-engineering.md)
