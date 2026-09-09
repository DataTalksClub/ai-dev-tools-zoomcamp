# Homework 2: Build and Ship an AI-Assisted Full-Stack App

In this homework, we'll build an end-to-end application with AI: a frontend, a backend, and a database.

You will need Python with `uv` for the backend and Node.js for the frontend. You don't need to know any of these technologies for doing this homework.

If some questions are not clear, or you're not sure which answer to select, ask your AI assistant to help.

## Question 1: Pick your project

You can choose one of the four project ideas:

- Expense splitter
- Restaurant waitlist manager
- Mini Kanban board
- Sports-league scoreboard

Pick the one you like most. The workflow is the same for all of them.

Which project did you choose for this homework?


## Question 2: Spec first

Like in homework 1, we start with a spec. 

Open a chat assistant and ask it to help you come up with the specification.

Answer its questions, then ask it to save everything to a markdown file.

Also ask it to help you come up with the name for this application. 
What's the name you chose?


## Question 3: GitHub Repository

Create a new GitHub repository (or a folder in the repository you used for Homework 1), clone it locally. Put the spec there:

- `_docs/specs.md` with the spec
- `.gitignore`
- `README.md`
- `AGENTS.md`

Commit and push. What's the sha1 hash for this commit?


## Question 4: Frontend prototype

Build a frontend prototype with a mocked backend. To make it simpler, use your coding agent directly, not Lovable (but you can experiment with it too). 

```text
Implement the frontend for the app described in _docs/specs.md. Put it in frontent/.

Don't implement the backend yet. Centralize all the backend calls
in one place and mock them for now.

Make the UI interactive so I can use the main features from the spec.
```

Iterate until you like the results.

Which command do you use to start the frontend?


## Question 5: Backend

Now let's create the backend. You can first ask your coding assistant to analyze the frontend code and create the specs, and then based on specs create the backend. Or you can create backend directly. 

Like in the lessons, we'll first create the backend with a mock database, make sure it integrates well with the frontend, and then replace it with a real database.

Your prompt may look like this:

```text
Based on openapi.yaml, create a FastAPI backend. Use uv for package management.
Use a mock database, we will replace it with a real one later.
Write tests for the endpoints first, then implement them.
```

Which command do you use to start the backend?

## Question 6: Connect frontend and backend

The backend now works (presumably) so let's connect frontent to it. Ask the coding assistant to do it.

You can verify that the connection works manually, but you can also ask your agent to use the browser to check it for you. 

Which URL does the frontend use to talk to the backend?

## Question 7: Database

Now the backend and frontend work fine, you can swap the mock store for a real database.

Keep the app database-agnostic and use SQLAlchemy for that.

Make sure test still pass and add more tests if needed. Ask your agent for recommendations.

Which command do you use for running tests?



## Submission

Submit your homework here: https://courses.datatalks.club/ai-dev-tools-2026/homework/hw2



## Learning in Public

We encourage everyone to share what they learned. This is called "learning in public". Read more about why it matters [here](https://aishippingblog.com/p/benefits-of-learning-in-public).

Don't worry about being perfect. Everyone starts somewhere, and people love following genuine learning journeys!

### Recording a Demo Video

Consider recording a short demo video of your application in action! This makes your post much more engaging and helps others see what you've built.

You can use:

- Screen recording tools like OBS Studio, QuickTime, or Windows Game Bar
- Loom for quick and shareable recording
- Snipping Tool on Windows

Keep it short (30-90 seconds) and show:

- The main user flow of your project, e.g. adding an expense and seeing who owes whom
- The same data from two browsers, e.g. a change made in one showing up in the other
- Data still being there after a refresh

Upload your video to LinkedIn, Twitter/X, or YouTube and share the link!

### Example post for LinkedIn:

```
🚀 Week 2 of AI Dev Tools Zoomcamp by @DataTalksClub complete!

Built a full-stack app with AI — spec first, then a frontend prototype, an OpenAPI contract, and a FastAPI backend, all with an AI coding agent!

Today I learned how to:

✅ Turn a product spec into a working app
✅ Use an OpenAPI contract as the source of truth between frontend and backend
✅ Implement a backend without knowing the framework
✅ Swap a mock database for SQLite
✅ Cover the app with tests

Here's my repo: <LINK>
Demo video: <VIDEO_LINK>

Following along with this amazing course - who else is building with AI?

You can sign up here: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/
```

### Example post for X:

```
🤖 Built a full-stack app with AI!

📝 Spec first, code second
🎨 Frontend prototype
📜 FastAPI backend
💾 SQLite
✅ Tests

My repo: <LINK>
Demo: <VIDEO_LINK>

Zero full-stack knowledge → working app in one week!

Join me: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/
```
