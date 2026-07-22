# Implementing a Task

Video: TBA

The issue is groomed, so now we write the code.

## Software engineer

The next role in the team is the one that does the implementation.

Add `software-engineer.md` next to `pm.md`:

```text
team/
  pm.md
  software-engineer.md
```

Here's what's inside:

```markdown
You're a Software Engineer

You implement one groomed task at a time.

- Read the issue and implement what it describes
- Implement against the acceptance criteria, do not change them
- Stay inside the files and constraints the issue names
- Write tests for what you built
- Do not close the issue
- Commit regularly

Definition of done:

- Every acceptance criterion in the issue is implemented
- Tests are written for the new behaviour, and the whole suite passes
- The work is committed
- The issue is still open, with a comment saying what you did

If an acceptance criterion is wrong, impossible, or contradicts
another one, create a comment on the issue about it.
```

And add it to `AGENTS.md`:

```markdown
Team

- To groom a task, follow `team/pm.md`
- To implement a task, follow `team/software-engineer.md`
```

Then start a fresh session:

```text
Implement issue #4
```


## Small steps

Make the agent work through it one change at a time, and make sure it commits after every major step.

Frequent commits give you a cheap way to go back. If the last commit was
five minutes ago, and something went wrong, throwing the current code away and rewinding is easy. If it
was an hour ago, you'll have to re-create it.

The engineer session ends when the code is written and its own tests
pass. That's not the same as the task being done - it's the agent
marking its own homework, which is what the next lesson is about.


[← Grooming a Task](06-grooming-a-task.md) | [Testing a Task →](08-testing-a-task.md)
