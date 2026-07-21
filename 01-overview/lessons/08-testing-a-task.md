# Testing a Task

Video: TBA

The code is written and the engineer says it works. But does it really work?

## The best tester is not the author

An agent that writes the code and then judges whether the code is
correct is grading its own homework.

By the time it finishes, it has spent its entire context convincing
itself that its approach was the right one. If you ask "is this correct?"
you will get "yes, this correctly handles the edge case". 

But the edge cases are only the ones that it thought of, handled the way it decided to handle it.

In software engineering teams we have QA engineers: people who specialize
on testing software.

We follow the same idea here: testing gets its own session, with no memory of
how the code was written, checking the result against the acceptance
criteria independently.

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

The "do not fix anything" rule keeps the roles apart. A QA
session that repairs the findings becomes the author
again, so you're back to marking your own homework.

A FAIL goes back as a new engineer session, with the QA comment as the
input. Then QA runs again. You repeat the process until it passes.

A PASS is what closes the issue.

"Mostly works, a couple of small things" is not the outcome, only `PASS` or `FAIL` are accepted.


Tests let you delegate the implementation to agents without reading every line.

## Test smells

Worth checking for, because agents produce all of these:

- The system under test is mocked. Everything the code touches is
  replaced by a stub, the test passes, and nothing real was exercised.
  This is the most common one, and the most useless.
- Assertions that cannot fail. Checking a page returned 200, or that a
  list is a list. Break the code on purpose and see the test go red -
  fifteen seconds, and it is the only way to know it is wired up.
- Testing the framework, not your code. Your ORM saves records. That is
  not your behaviour, and it is not your test.
- Assertions against a whole blob of output. Comparing an entire HTML
  body or JSON dump breaks on every unrelated change and tells you
  nothing about which part mattered.
- Hardcoded waits in browser tests. A `sleep(2)` is a test that fails
  on a slow machine and passes on a fast one, regardless of the code.
- Tests deleted or weakened to go green. When an agent is told "make
  the tests pass", removing the failing test satisfies the instruction
  it was given. So does loosening an assertion or adding a skip. Check
  what disappeared, not only what was added.

The deeper problem underneath several of these: if the same agent, in
the same session, wrote both the implementation and the test, they can
encode the same misunderstanding. The test passes because it asserts
what the code does, rather than what the code should do.

## Three ways out

1. Write the acceptance test before the feature exists. The criteria in
   the issue came from grooming, before anyone implemented anything, so
   a test derived from them is checking your intent rather than the
   implementation.
2. Test-driven development. Same idea, tighter loop - failing test
   first, then the code that passes it. Agents are good at this when
   you ask for it explicitly.
3. Tests written after the implementation are fine too, as long as you
   know that is what they are. They protect against future change. They
   do not tell you the current behaviour is correct.

Most work is the third case. That is not a problem, as long as nobody
mistakes a green suite for a verified feature.

## CI

Everything here runs on your machine, when you remember. Running the
same checks automatically on every push is what stops "it works
locally" from being the last word.

That belongs to [Module 2](../../02-end-to-end/), along with
deployment.

[← Implementing a Task](07-implementing-a-task.md) | [Loop Engineering →](09-loop-engineering.md)
