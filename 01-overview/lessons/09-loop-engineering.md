# Loop Engineering

Video: TBA

So far you have typed every prompt yourself, running three sessions per
task to groom, implement, and test.

That's the right way to learn it, but it doesn't scale to many issues.

Loop engineering helps with that.

Loop engineering is designing the system that runs a coding agent
repeatedly, instead of driving the agent prompt by prompt.

The "system" is the harness that controls your agent, plus whatever you
wrap around it. It decides what the agent picks up next, checks the
result, and decides whether to go again.


## The ladder

Loop engineering is usually presented as one step on a ladder:

- Prompt engineering - what you say in one message
- Context engineering - what the agent knows before it starts
- Loop engineering - how often it runs, on what, and when it stops
- Graph engineering - who does what, when there's more than one agent

In June 2026 Addy Osmani published the [Loop Engineering essay](https://addyo.substack.com/p/loop-engineering) that gave it a name and Peter Steinberger compressed the whole idea into one
sentence:

> stop prompting your agents and start designing the loops that
> prompt them.

TODO - screenshots of the original X posts

Many harnesses have built-in support for loops like
`/goal`, `/loop` and `/schedule`.

That's what puts this term on firmer ground than the one in the next
lesson. The vendors shipped features for it, rather than only arguing
about it on X.

## /goal in practice

The simplest useful loop is one command:

```text
/goal all tests pass
```

The agent works, runs the suite, and reads the failures. It works again
and stops when the suite is green or it hits the turn limit. You're not
in that cycle.

Something more realistic for our project:

```text
/goal refactor src/cost so no file is over 200 lines, tests stay green
```

The stop condition has to be something a model can evaluate: "all tests
pass" is checkable, and so is "no file over 200 lines".

"Make the code better" isn't checkable, so your agent can run forever (or stop too early).

## Building the loop yourself

Many harnesses have the primitives you need to implement loops:

- Claude Code has `/goal` and `/loop`
- Codex only has `/goal`

But some harnesses may not have it, so it could be useful to know how to write them yourself.

You need these:

- Stop hooks. A hook that fires when the agent finishes a turn can
  check a condition and prompt it again, which is how you implement `/goal`.
- Scheduled pings into a tmux session. If the agent is running in tmux,
  you can send keystrokes to that session on a timer, which is how you implement `/loop`.


[← Testing a Task](08-testing-a-task.md) | [Graph Engineering →](10-graph-engineering.md)
