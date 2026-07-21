# Steering a Session

Video: TBA

Lesson 5 was about what the agent knows before it starts. This lesson
is about the twenty minutes after you press enter: a live conversation
with something fast, literal, and willing to keep going in a wrong
direction for as long as you let it. Steering it is a skill, and it's
made of small habits rather than clever prompts.

## The loop

Here is the shape of the work. It doesn't change much between tools:

```text
spec -> context -> plan -> edit -> run -> test -> inspect diff -> review -> commit
```

let's remove inspect diff - the review is done by another agent 
and let's see how to incoporate it into the flow we have 
I also don't like the name, so let's remove it and take the relevant parts from here
to other lessons

Nobody disagrees with that diagram, and it looks obvious enough to
skip. But the diagram is not the interesting part. What matters is what
you do at each arrow: whether you look at the plan before the edits,
how big a step you allow between commits, how fast you interrupt when
it goes wrong, and when you decide to stop entirely. That's the
difference between a session that lands and one that burns an hour, and
the rest of this lesson is those habits.

## Plan before edits

This is the single highest-leverage habit in the lesson, so it goes
first. Before the agent touches a file, ask it what it intends to do
and which files it intends to change. Not a vague description - an
actual list of steps and an actual list of paths.

Most tools now have a mode for this - a plan mode, a read-only mode, an
ask mode, a "propose changes first" setting. The names differ and
change often, so find the one in your tool and learn its shortcut. The
idea is the same everywhere: let it read and think, don't let it write
yet.

Why it pays off is arithmetic. You ask for a pause key in the Snake
game, and reading the plan back takes about a minute:

```text
1. Add a `paused` flag to the game state       game.py
2. Handle the space key in the input loop      input.py
3. Skip the update tick while paused           game.py
4. Add a test for pause and resume             tests/test_game.py
```

You can see from that list whether it understood you. If it were about
to rewrite the renderer, or touch six files you didn't expect, you know
now, and correcting it costs one sentence. Reviewing a bad hundred-line
diff instead takes fifteen minutes, because you have to reconstruct the
intent from the code first. The plan also gives you something to check
the result against: when the diff arrives, you're not asking "is this
good?" in the abstract, you're asking "is this the four things it said
it would do?"

## Small steps

One change at a time, committed. The temptation runs the other way: the
agent is fast, so you write a prompt with five things in it and it does
all five. Then something is broken, and you have a diff touching nine
files with no idea which of the five changes caused it.

Large unreviewed batches are where control is lost. Not dramatically -
you gradually stop reading, because reading has become expensive, and
once you stop reading you're back to vibe coding with more steps.

Frequent commits also give you a cheap way back. If the last commit was
five minutes ago, throwing away the current mess costs nothing. If it
was an hour ago, you'll try to rescue it, which is usually the wrong
call. So the inner rhythm is: one change, run it, read the diff,
commit, next. Commit messages can be the agent's job. Deciding what
belongs in one commit is yours.

## Course-correcting

When you see the first response going the wrong way, stop it. There's a
real instinct to let it finish - it feels rude to interrupt, and you
feel you should see the whole answer before judging it. That instinct
is expensive. You're not being rude to anyone, and every extra second
in a wrong direction is more tokens spent and more code you'll have to
read and discard. Interrupt early. Every interactive tool lets you.

The second half matters more. Once you've stopped it, resist the urge
to patch. The common failure looks like this:

```text
you:   add pause
agent: [starts rewriting the input system]
you:   no, don't rewrite the input system
you:   also keep the existing key handler
you:   actually revert that part
```

Each follow-up is a correction stacked on a bad foundation, and all of
them stay in the context, arguing with each other. The result is a
confused agent and a conversation you can no longer read.

Re-frame instead. Go back, rewrite the original request with the
constraint you now know was missing, and start that step again. "Add a
pause key. Use the existing key handler in `input.py`, don't change how
input is dispatched." One clear instruction beats four corrections, and
writing a third correction is the signal that you need one.

## Long sessions degrade

we will start every task in a new session 
and then later introduce subagents and do that there

A long session is not a better-informed session. As the context fills
up, quality drops. The agent starts forgetting constraints you set
forty messages ago, reintroduces things you told it to remove, and gets
vaguer about what the task was. It feels like the agent has become
worse at its job. What actually happened is that the conversation
became a large, noisy document, and everything from lesson 5 about
signal and noise applies to it.

Practical responses, in order of usefulness:

- **Start a fresh session for a new task.** The cheapest fix by far.
  If what you're doing now has nothing to do with what you were doing
  an hour ago, that hour of history is pure noise.
- **Summarise deliberately.** If you do need to carry state across,
  write the summary yourself, or ask for one and edit it. Most tools
  can compact a conversation automatically, which is fine, but the tool
  is guessing at what mattered. You know.
- **Put durable things in `AGENTS.md`, not in the chat.** Anything you
  repeat session after session isn't a message, it's project context.
  That's what the module deliverable is for.

Tools also offer ways to rewind a session to an earlier point. Learn
what yours has. The idea behind all of it is the same: the conversation
is a resource you manage, not a log that accumulates.

## Autonomy levels

let's do this earlier 
and say that you choose the level that's confortable for you
loop and graph engineering are advanced thisgs that require the skip permissions mode so you ahve to be confrortable with agent workign completely autonomously

There's a spectrum between approving every action and letting the agent
run unattended:

```text
approve every step  ->  approve writes  ->  auto within a scope  ->  unattended
```

None of these is the correct setting. It's a per-task choice, and it
depends on two things: how reversible the work is, and how well you can
check the result.

| Situation | Autonomy |
|---|---|
| Local code, good tests, clean git state | High |
| Refactor in a well-covered module | High |
| New feature in unfamiliar code | Medium |
| Anything touching auth, secrets or permissions | Low |
| CI config, deployment, infrastructure | Low |
| Migrations or anything that writes to real data | Low |

The right-hand column is not "how hard is this". It's "what happens if
it's wrong and nothing catches it". A bad refactor in a tested module
fails loudly in ten seconds and `git checkout` undoes it. A bad
migration doesn't, and neither does a leaked secret.

Being on a branch with a clean working tree moves almost everything up
a level, which is another reason the small-steps habit pays for itself.
Lesson 8 sharpens this into one line: the autonomy ceiling is set by
verification reach.

## Knowing when to stop

If the agent has failed at the same thing three times, a fourth attempt
will probably fail too. Worth stating plainly, because the sunk cost is
real and persuasive. You've spent thirty minutes, it's *almost*
working, the last error looks smaller than the one before, so you send
it again. The failure mode isn't dramatic. It's an afternoon.

Three strikes and you change something:

- **Simplify the task.** Ask for a smaller piece. Often the agent is
  stuck because the request bundled two problems together.
- **Do the hard part yourself.** Write the tricky function by hand and
  hand the rest back. Ten minutes of your own typing can unblock
  something that resisted five prompts.
- **Change the approach.** If it can't make the chosen design work, the
  design may be the problem, not the agent.
- **Check your own inputs.** The third failure may be telling you the
  spec was ambiguous, or the context was missing a file it needed.

What doesn't work is repeating the same prompt with more emphasis. The
model is not holding back effort.

## What to take from this

Six habits, and none of them are about prompt wording:

1. See the plan before the edits.
2. One change at a time, committed.
3. Interrupt early, then re-frame rather than patch.
4. Treat a long session as a liability, not an asset.
5. Pick autonomy per task, based on reversibility.
6. Stop after three failures and change something.

Together they answer the second of the three questions from lesson 1:
what actually changed? You can only answer that if you kept the session
small enough to follow. Next: how you know the result is right, which
is the third question.

[← Context Engineering](05-context-engineering.md) | [Tests and Verification →](07-tests-and-verification.md)
