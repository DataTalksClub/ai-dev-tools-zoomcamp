# Grooming a Task

Video: TBA

[Lesson 3](03-specs.md) made the case that the quality of what an agent
builds is decided before it writes any code. [Lesson 4](04-bootstrapping.md) turned the spec into a backlog.

Those backlog items are still rough. A task like "add attendees" is a
placeholder - it names the work without saying what done looks like.
Grooming is the step that turns it into something an engineer can
implement without asking you a single question.

It is the same idea as in lesson 3, but for an individual task, not the entire project.

## Product manager

In a product team, usually grooming is the reponsibility of the Product Manager. So let's have our own product manager who will be responsible for that. 

Create a `team/` folder and create the `pm.md` file:

```text
team/
  pm.md
```

Here's what's inside:

```markdown
You're a Product Manager

You groom a task before anyone implements it.

- Read the issue as written
- Rewrite it using the template in `team/task-template.md`
- Make the acceptance criteria checkable - someone should be able to
  point at the screen and say yes or no
- Think about the edge cases the person who filed it did not
- Do not write any code

Definition of done:

- The issue has all four sections filled in
- Every acceptance criterion can be checked by looking at the result
- Everything moved out of scope links to a follow-up issue
- An engineer who has never spoken to you could implement it from the
  issue alone

If something does not belong in this task, do not silently drop it - file a follow-up issue, and list it under out of scope with a link to that issue, so it
is clear what was moved and where it went.
```

## The task template

The PM needs a shape to fill in, so a groomed issue always looks the
same. Put it in `team/task-template.md`:

```markdown
## Goal

One or two sentences on what should be true when this is done.

## Acceptance criteria

- [ ] A statement you can check by looking at the result
- [ ] One line per case, including the awkward ones

## Out of scope

- Something that does not belong in this task, moved to #12

## Constraints

- Files this should stay inside
- Libraries it may not add, patterns it must follow
```

Checkboxes are worth the two extra characters. They give the QA session
in [lesson 8](08-testing-a-task.md) a list to tick off one by one, and
they make an unfinished task visible at a glance.

Link the folder from `AGENTS.md`, the same way as the `_docs` files in
[lesson 5](05-context-engineering.md):

```markdown
Team

- To groom a task, follow `team/pm.md`
```

The agent learns the role exists when it starts, and opens the file
when you ask it to groom something.

## Running the session

Start a fresh session:

```text
Groom issue #4
```

It's important to read and understand the result. Do not skip this.

Grooming is the cheapest place in the whole process
to catch a misunderstanding: the issue is a paragraph, and correcting
it costs one sentence.

The same misunderstanding found after
implementation costs a rewrite, and found after release costs
considerably more.

Four things to check:

- Does the goal match what you actually wanted?
- Is every acceptance criterion something you could check?
- What got scoped out?

If the groomed issue surprises you, fix the result.


[← Context Engineering](05-context-engineering.md) | [Implementing a Task →](07-implementing-a-task.md)
