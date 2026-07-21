# Loop Engineering

Video: TBA

So far we have typed every prompt yourself. Three sessions per task -
groom, implement, test.

That is the right way to learn it, but it doesn't scale to many issues.

Loop engineering helps with that.

Loop engineering is designing the system that runs a coding agent
repeatedly, instead of driving the agent prompt by prompt.

The "system" is the harness that controls your agent and
whatever you wrap around it: the thing that decides what the agent
picks up next, checks the result, and decides whether to go again.


## The ladder

Loop engineering is usually presented as one step on a ladder:

- Prompt engineering - what you say in one message
- Context engineering - what the agent knows before it starts
- Loop engineering - how often it runs, on what, and when it stops
- Graph engineering - who does what, when there is more than one agent

In June 2026 Addy Osmani published the [Loop Engineering essay](https://addyo.substack.com/p/loop-engineering) that gave it a name and Peter Steinberger compressed the whole idea into one
sentence:

> stop prompting your agents and start designing the loops that
> prompt them.

TODO: screenshots of the original X posts

Many harnesses have build-in support for loops like
`/goal`, `/loop` and `/schedule`.

That is what puts this term on firmer ground than the one in the next
lesson. The vendors shipped features for it, rather than only arguing
about it on X.

## /goal in practice

The simplest useful loop is one command:

```text
/goal all tests pass
```

The agent works, runs the suite, reads the failures, works again, and
stops when the suite is green or it hits the turn limit. You are not in
that cycle.

Something more realistic for our project:

```text
/goal refactor src/cost so no file is over 200 lines, tests stay green
```

The stop condition is
something a model  can evaluate. "All tests pass" is checkable. "No
file over 200 lines" is checkable.

"Make the code better" is checkable, so your agent can run forever (or stop too early).

## Building the loop yourself

Many harnesses have the primitives you need to implement loops:

- Claude Code has `/goal` and `/loop`
- Codex only has `/goal`

But some harnesses may not have it, so it could be useful to know how to write them yourself. 

You need these:

- Stop hooks. A hook that fires when the agent finishes a turn can
  check a condition and prompt it again. You can implement `/goal` this way.
- Scheduled pings into a tmux session. If the agent is running in tmux,
  you can send keystrokes to that session on a timer. This way you can implemnet `/loop`. 


[← Testing a Task](08-testing-a-task.md) | [Graph Engineering →](10-graph-engineering.md)
