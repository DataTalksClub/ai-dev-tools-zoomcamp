# Homework 1: AI-Native Developer Workflow

In this homework, we'll build an application with AI — but instead of us handing you a finished spec, you'll turn a vague idea into one yourself, then implement it in Django.

You can use any coding agent you want: Claude Code, Codex CLI, Gemini CLI, Cursor, Aider, GitHub Copilot, etc. Pick **one** and stick with it for the whole homework — with chat-based tools you'd need to copy code back and forth, so we recommend an agent that can edit files and run commands directly in your homework repository.

You will only need Python to get started (we also recommend that you use `uv`). You don't need to know Python or Django for doing this homework.

## Homework Idea

For this homework, we start with a very vague idea:

> A tool for managing shared household chores

We don't specify anything else, and most of you will finish with different homework solutions.

In this homework, we want to turn this vague description into a clear specification.


## Question 1: Select your coding agent

You can use any coding agent you want. Which one did you choose? 


## Question 2: Turn the idea into a spec

Open a chat assistant and brainstorm with a prompt like:

```text
I want to build a tool for managing shared household chores.

Help me set the scope for this homework precisely. I want to brainstorm with you
and understand how the tool should work. Give me options.

Ask me one question at a time and keep your output short.
```

Answer its questions, then ask it to save everything to a markdown file. 

What are the 2-4 features your spec settled on?

## GitHub Repository

Create an empty GitHub repository, clone it locally. Create two files there:

- `.gitignore`
- `README.md`
- `_docs/plan.md` with the plan

Commit and push.

## Question 3: Django project

For this homework we'll use Django. 

Ask your agent to install Django and create a project and an app for it. At some point, you will need to include the app you created in the project.

What's the file you need to edit for that?

- `settings.py`
- `manage.py`
- `urls.py`
- `wsgi.py`

For this and next questions you can ask your coding assistant to select the correct option.


## Question 4: Backlog

Then give your agent the `plan.md` and ask it to propose a small backlog of tasks for building this in Django. Write the result to `backlog.md`.

What's task 1 in the backlog your agent came up with?


## Question 5: First version

Implement the first few tasks. Just open your agent and say:

```
Implement task #1 from backlog.md
```

Run the server. Which command do you use to start the Django development server?

- `uv run python manage.py runserver`
- `uv run django-admin startserver`
- `python manage.py start`
- `uv run python app.py runserver`



## Question 6: Tests

After implementing a few items from the backlog, let's make sure the code is covered with tests. 

- Tell the agent we want to cover the code with tests
- Ask it which scenarios we should cover
- Make sure they make sense
- Let it implement them and run them

What's the command you use for running tests in the terminal?

- `pytest`
- `python manage.py test`
- `python -m django run_tests`
- `django-admin test`


## Submission

Submit your homework here: https://courses.datatalks.club/ai-dev-tools-2026/homework/hw1

Use the link to repository you created in the homework submission form.

## Learning in Public

We encourage everyone to share what they learned. This is called "learning in public". Read more about why it matters here: https://aishippingblog.com/p/benefits-of-learning-in-public

Learning in public is one of the most effective ways to accelerate your growth. Here's why:

1. Accountability: Sharing your progress creates commitment and motivation to continue
2. Feedback: The community can provide valuable suggestions and corrections
3. Networking: You'll connect with like-minded people and potential collaborators
4. Documentation: Your posts become a learning journal you can reference later
5. Opportunities: Employers and clients often discover talent through public learning

Don't worry about being perfect. Everyone starts somewhere, and people love following genuine learning journeys!

### Example post for LinkedIn:

```
🚀 Week 1 of AI Dev Tools Zoomcamp by @DataTalksClub complete!

Turned a vague one-line idea into a spec, broke it into a backlog, and let an AI coding agent build a Django app for managing shared household chores!

Today I learned how to:

✅ Turn a vague idea into a written spec
✅ Break a spec into a backlog of tasks
✅ Set up a Django project and app with AI
✅ Implement backlog tasks one at a time with a coding agent
✅ Cover the app with tests

Here's my repo: <LINK>

Following along with this amazing course - who else is exploring AI development tools?

You can sign up here: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/
```

### Example post for Twitter/X:


```
🤖 Built a Django app with AI in @Al_Grigor's AI Dev Tools Zoomcamp!

📝 Spec first, code second
🗂️ Backlog-driven implementation
✨ Household chores app from scratch
✅ Tests

My repo: <LINK>

Zero Django knowledge → working app in one session!

Join me: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/
```
