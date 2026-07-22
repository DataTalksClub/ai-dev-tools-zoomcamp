# Testing a Task

Video: TBA

The code is written and the engineer says it works. Now we check whether that's true.

## The best tester is not the author

An agent that writes the code and then judges whether the code is
correct is grading its own homework.

By the time it finishes, it has spent its entire context building the
case that its approach was the right one. If you ask "is this correct?"
you'll get "yes, this correctly handles the edge case".

But the edge cases are only the ones that it thought of, handled the way it decided to handle it.

In software engineering teams we have QA engineers: people who specialize
on testing software.

We follow the same idea here. Testing gets its own session, with no
memory of how the code was written. It checks the result against the
acceptance criteria independently.

## QA engineer

Add `qa-engineer.md` to the team:

```text
team/
  pm.md
  software-engineer.md
  qa-engineer.md
```

Here's what's inside:

```markdown
You're a QA Engineer

You check finished work against the issue that specified it.

- Read the acceptance criteria from the issue
- Check each one against what the code actually does
- Run the tests, and say which ones you ran
- Look for the cases the criteria describe but the tests do not cover
- Do not fix anything you find. Report it by creating a comment

Your output is a verdict: PASS or FAIL. It is FAIL if a single
acceptance criterion fails. Post it as a comment on the issue:

## QA: FAIL

- [x] Salary is entered as an annual figure - PASS
- [ ] Removing an attendee stops their cost accruing - FAIL
      Removed someone mid-meeting, the total kept rising

Tests: `npm test`, 14 passed, 0 failed

Definition of done:

- The comment starts with PASS or FAIL
- Every acceptance criterion has a verdict against it
- Every FAIL says what you did and what happened
- The test command and its result are included
- Nothing in the code was changed

Ignore what the implementation says it does. Only the acceptance
criteria and the running code count.
```

And add it to `AGENTS.md`:

```markdown
Team

- To groom a task, follow `team/pm.md`
- To implement a task, follow `team/software-engineer.md`
- To test a task, follow `team/qa-engineer.md`
```

Then, in a new session:

```text
Verify issue #4
```

## Tests as the guardrail

The "don't fix anything" rule keeps the roles apart. A QA
session that repairs the findings becomes the author
again, so you're back to marking your own homework.

A FAIL goes back as a new engineer session, with the QA comment as the
input. Then QA runs again. You repeat the process until it passes.

You close the issue only on a PASS.

"Mostly works, a couple of small things" isn't an outcome. Only `PASS` or `FAIL` are accepted.


Tests let you delegate the implementation to agents without reading every line.


[← Implementing a Task](07-implementing-a-task.md) | [Loop Engineering →](09-loop-engineering.md)
