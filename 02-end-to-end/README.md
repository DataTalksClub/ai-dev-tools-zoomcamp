# Module 2 — End-to-End Application (Snake)

## Overview

[🎥 Video](https://www.youtube.com/watch?v=vMNJru1y2Uc&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)

In this module, we will create an end-to-end application using AI:

- create frontent with Lovable and React
- extract OpenAPI specs from the frontend 
- implement backend with FastAPI based on the specs
- add database support to the backend
- containerize everything
- deploy to Render
- create a CI/CD pipeline with tests and deployment

You will find all the code here: https://github.com/alexeygrigorev/snake-arena-online

## Frontend

[🎥 Video](https://www.youtube.com/watch?v=F1XJuV1V-BU&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)

First we will start with implementing frontend with Lovable.

You can choose any other tool (Bootraper like Bolt, or AI Assistant like Cursor, Claude Code, Codex, Copilot or Antigravity)

For Lovable, I used this prompt:

> create the snake game with two models: pass-through and walls. prepare to make it multiplayers - we will have this functionality: leaderboard and watching (me following other players that currently play). add mockups for that and also for log in.
> everything should be interactive - I can log in, sign up, see my username when I'm logged in, see leaderboard, see
> other people play (in this case just implement some playing logic yourself as if somebody is playing) 
> make sure that all the logic is covered with tests 
> 
> don't implement backend, so everything is mocked. But centralize all the calls to the backend in one place

Create the frontend and put it to Github.


## (Optional) Connecting Antigravity to Codespaces

[🎥 Video](https://www.youtube.com/watch?v=D7vrd8SJENg&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)


For the rest of the videos, I'll use 
[Google Antrigravity](https://antigravity.google/) as the AI assistant and [Codespaces](https://github.com/features/codespaces) as the environment.

If you want to have the same setup, in this section I'll show how to connect Antigravity to Codespaces. These instructions work for Cursor too.

If you use Copilot or Codex, you don't need it - just use VS Code to connect to Codespaces.

If you run things locally, you also don't need it. But you need to have NodeJS, Python and Docker installed (Codespaces already have them). 

Step 1: Install GitHub CLI

* Download from: https://github.com/cli/cli/releases

Step 2: Authenticate

```bash
# Authenticate with GitHub using SSH
gh auth login
# Select: SSH protocol and your existing SSH key for GitHub
# Follow the remaining prompts

# authenticate for codespaces
gh auth refresh -h github.com -s codespace
```

Step 3: Create and Use Codespace

```bash
gh codespace create
# Note the ID that's generated (e.g., expert-doodle-wr7wg9p5gqcgggw)
```

Step 4: Connect via SSH

```bash
gh codespace ssh -c expert-doodle-wr7wg9p5gqcgggw
```

Next, get the SSH config:

```bash
gh codespace ssh --config -c expert-doodle-wr7wg9p5gqcgggw
```

Add the output to `~/.ssh/config`

**If you encounter "cannot find the key" error:**

```bash
ssh-keygen -t ed25519 -f ~/.ssh/codespaces.auto
ssh <codespace-name>
```

Step 5: Use with Antigravity

- Connect to codespace using Antigravity's SSH remote mode
- Open the project folder in `/workspaces/`

Step 6: Stop Codespace When Done

```bash
gh cs stop -c expert-doodle-wr7wg9p5gqcgggw
```


## Running and Testing the Frontend Locally

* [🎥 Video #1 (starting from 12:00)](https://www.youtube.com/watch?v=D7vrd8SJENg&t=719&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)
* [🎥 Video #2 about tests](https://www.youtube.com/watch?v=xbsV_RarTUM&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)


Run the Application:

```bash
# Install dependencies and start the development server
npm install
npm run dev
```

Run Tests:

```bash
npm test
```


## Creating the Backend

[🎥 Video](https://www.youtube.com/watch?v=jHVbbw-v_zY&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)


First, move all frontend files into a dedicated folder:

```bash
mkdir frontend
mv * frontend/
```

Next, we will generate the OpenAPI Specifications

OpenAPI specifications provide a standardized way to define REST APIs, enabling automatic documentation generation, client/server code generation, and ensuring contract consistency between frontend and backend.

Let's create it:

> analyse the content of the client and create an OpenAPI specs based on what it needs. later we want to implement backend based on these specs

Now we're ready to create the backend project:

```bash
pip install uv
mkdir backend && cd backend
uv init
```

AI Agents don't know how to properly use `uv` (it's a relatively new tool). So we need to tell them how to use it. We typically use the `AGENTS.md` file for that.

Let's create it: 

```markdown
For backend development, use `uv` for dependency management.

Useful Commands

    # Sync dependencies from lockfile
    uv sync

    # Add a new package
    uv add <PACKAGE-NAME>

    # Run Python files
    uv run python <PYTHON-FILE>
```

**Note:** At the moment of creating this course, Antigravity doesn't automatically follow the instuctions in AGENTS.md. Until they fix it, ask it explicitly to follow these guidelines.

Now let's create the backend. The prompt:

> based on the OpenAPI specs, create fastapi backend 
> for now use a mock database, which we will later replace with a real one
> create tests to make sure the implementation works
> 
> follow the guidelines in AGENTS.md

Additionally, you can ask AI to implement a `verify_api.py` script that tests the running server to ensure all endpoints work correctly.


## Integrating Frontend and Backend

[🎥 Video](https://www.youtube.com/watch?v=Y46XU8MYnmY&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)


We now have backend. Lets connect it to frontend. Prompt:

> Make frontend use backend. use OpenAPI specs for guidance
> follow the guidelines in AGENTS.md

We also need a way to run them both at the same tile. Prompt: 

> How can I run both frontend and backend at the same time? 
> Let's use concurrently instead of our own script

If you have an error, just tell AI to fix it. For example, during preparation, when I tried to create an account in the app, it would show an error message saying "Not Found". Here's how I fixed it:

> I tried creating an account and it says Not Found
> write a test on backend to reproduce it, fix it, and make sure the frontend works fine too

## Database Support

* [🎥 Video (Adding database)](https://www.youtube.com/watch?v=q8r_ugvQxEE&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)
* [🎥 Video (Integration tests)](https://www.youtube.com/watch?v=kfEjwDD5Vv8&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)

Our backend uses a mock database. Let's use a real one now. Prompt:
> now for backend let's use postgres and sqlite database (via sqlalchemy) 
> follow the guidelines in AGENTS.md

And don't forget about tests for the database layer:

> let's also add some integration tests (using sqlite) to make sure things work 
> put the integration test in a separate folder tests_integration


## Containerization with Docker

[🎥 Video (Containerization)](https://www.youtube.com/watch?v=mftbW-QXFRI&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)


It works with SQLite, but how about Postgres? Let's containerize everything 
and also add Postgres support: 

> right now we have frontend, backend, and database (sqlite)
> 
> let's put everything into docker compose and use postgres there. we can serve frontend with nginx or whatever you recommend

Run it:

```bash
docker-compose up --build
```

Stop when done:

```bash
docker-compose down
```


## Deloyment

[🎥 Video](https://www.youtube.com/watch?v=Y7OnXqYs30k&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)

For deployment we need a single container with both frontend and backend. 
Let's ask AI to put them together:

> For deployment we need to put together backend
> and frontend in one container. let's do that

And then ask:

> I want to deploy it to the cloud now. what are the options

My answer:

> let's go with render

## CI/CD

[🎥 Video](https://www.youtube.com/watch?v=lcmP9YCUmYw&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)


Prompt:

> I want to create a CI/CD pipeline with github actions with two parts
> 
> - first we run tests (frontend + backend)
> - if tests pass, I want to deploy the update to render

We also want to add integration tests:

> let's also run integration tests for backend separately before running deployment

If you 


## Cleanup

Don't forget to stop codespaces:


```bash
gh cs stop -c <CODESPACE_NAME>
```

Also if you deployed your application to the cloud, don't forget to delete your instances when you no longer need them.


## Community notes

Did you take notes? You can share them here

* Add a link to your notes above this line

