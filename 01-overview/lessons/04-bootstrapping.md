# Bootstrapping a Project

Video: TBA

You have a spec. This lesson turns it into a repo with a backlog the
agent can work through.

## The empty folder

Make a folder, initialise git, and drop the spec in.

```bash
mkdir project-name && cd project-name
git init
mkdir _docs
mv ~/Downloads/plan.md _docs/plan.md
```

## Decompose the spec


```text
Read plan.md. Propose a backlog of tasks that would implement it.

Each task should be small enough to finish in one session, and
independent enough that I could hand it to someone who has not read
the others. For each one give me a goal, acceptance criteria, what is
out of scope, and any constraints.

Do not write any code yet.
```

If you haven't decided what the tech stack for this project is, you should also do it.

TODO how to modify the prompt


Next, you should look at these tasks. Are they granular enough but not too granular? Do they make sense? You first need to review them. 

You can decide to merge some tasks into a bigger ones, or split big ones into smaller tasks. Or say that some things are out of scope. The planning you did previously will help, and if you're not sure about some things, discuss them with your coding assitant. 

## What a good task looks like

1. Goal - one or two sentences on what should be true afterwards.
2. Acceptance criteria - checkable statements. Not "works well" but
   things where you can point at the screen and say yes or no.
3. Out of scope - what this change must not do.
4. Constraints - files it should stay inside, libraries it may not
   add, patterns it must follow.

If a task takes more than a few minutes to write down, it is too big.
Split it.

Here is a whole task from the meeting cost calculator backlog:

```markdown
# Pause the meeting

## Goal
The running meeting can be paused and resumed, so a break does not get
billed.

## Acceptance criteria
- Pausing stops the cost increasing, and the displayed total stays put
- Resuming continues from exactly the total shown, nothing is added for
  the paused period
- The elapsed time and the cost stay consistent with each other after
  any number of pauses
- Pausing before the meeting has started does nothing
- The current state, running or paused, is visible on screen

## Out of scope
- No history of pauses, no breakdown of paused time
- Do not touch the attendee list or the rate calculation

## Constraints
- Changes stay in the timer and cost modules
- Do not add a library for this
```


## Put the backlog in GitHub issues

After we decomposed the specs into backlog, we need to persist it.

GitHub issues work well for this, and the agent can create them:

```text
Create a GitHub issue for each task, using the four sections. Label
them so I can see the order you would do them in.
```

For that to work, you need to have authenticated `gh` cli tool. 


[← Specs Before Code](03-specs.md) | [Context Engineering →](05-context-engineering.md)
