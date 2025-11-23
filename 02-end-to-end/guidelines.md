# End-to-End Development

In this module, we will create an end-to-end application using AI.

## Frontend

First we will start with implementing frontend with Lovable.

You can choose any other tool (Bootraper like Bolt, or AI Assistant like Cursor, Claude Code, Codex, Copilot or Antigravity)

For Lovable, I used this prompt:

```
create the snake game with two models: pass-through and walls. prepare to make it multiplayers - we will have this functionality: leaderboard and watching (me following other players that currently play). add mockups for that and also for log in.
everything should be interactive - I can log in, sign up, see my username when I'm logged in, see leaderboard, see
other people play (in this case just implement some playing logic yourself as if somebody is playing) 
make sure that all the logic is covered with tests 

don't implement backend, so everything is mocked. But centralize all the calls to the backend in one place
```

Create the frontend and put it to Github.


## (Optional) Connecting Antigravity to Codespaces

For the rest of the videos, I'll use Google Antrigravity as the AI assistant and Codespaces 
as the environment.

If you want to have the same setup, in this section I'll show how to connect Antigravity to Codespaces. These instructions work for Cursor too.

If you use Copilot or Codex, you don't need it - just use VS Code to connect to Codespaces.

If you run things locally, you also don't need it. But you need to have NodeJS, Python and Docker installed (Codespaces already have them). 

### Step 1: Install GitHub CLI

Download from: https://github.com/cli/cli/releases

### Step 2: Authenticate with GitHub

```bash
# Authenticate with GitHub using SSH
gh auth login
# Select: SSH protocol
# Select: your existing SSH key for GitHub
# Follow the remaining prompts
```

### Step 3: Authenticate for Codespaces

```bash
# filepath: terminal
# Check if codespaces authentication is needed
gh codespace list

# Refresh authentication with codespace scope
gh auth refresh -h github.com -s codespace
```

### Step 4: Create and Use Codespace

```bash
# filepath: terminal
# Create a new codespace for your exported Lovable repo
gh codespace create
# Note the ID that's generated (e.g., expert-doodle-wr7wg9p5gqcgggw)
```

### Step 5: Connect via SSH

```bash
# filepath: terminal
# Connect interactively
gh codespace ssh

# Or get SSH config for specific codespace
gh codespace ssh --config -c expert-doodle-wr7wg9p5gqcgggw
# Add the output to ~/.ssh/config
```

**If you encounter "cannot find the key" error:**

```bash
# filepath: terminal
# Create the required SSH key
ssh-keygen -t ed25519 -f ~/.ssh/codespaces.auto

# Test the connection
ssh <codespace-name>
```

### Step 6: Use with Antigravity

- Connect to codespace using Antigravity's SSH remote mode
- Open the project folder in `/workspaces/`

### Step 7: Stop Codespace When Done

```bash
# filepath: terminal
# Stop the codespace to save resources
gh cs stop -c expert-doodle-wr7wg9p5gqcgggw
```


## Running the Frontend Locally

### Run the Application

```bash
# filepath: terminal
# Install dependencies and start the development server
npm install
npm run dev
```

### Run Tests

```bash
# filepath: terminal
# Execute the test suite
npm test
```

---

## Creating the Backend

### Step 1: Reorganize Project Structure

Move all frontend files into a dedicated folder:

```bash
# filepath: terminal
# Create frontend directory
mkdir frontend

# Move all files to frontend folder
mv * frontend/
```

### Step 2: Generate OpenAPI Specifications

**Why OpenAPI?** OpenAPI specifications provide a standardized way to define REST APIs, enabling automatic documentation generation, client/server code generation, and ensuring contract consistency between frontend and backend.

**Prompt for AI Assistant:**

```
analyse the content of the client and create an OpenAPI specs based on what it needs. later we want to implement backend based on these specs
```

### Step 3: Initialize Backend Project

```bash
# Install uv package manager
pip install uv

# Create and navigate to backend directory
mkdir backend && cd backend

# Initialize Python project with uv
uv init
```

### Step 4: Create Agent Guidelines

Create a file with instructions for AI assistants:

```markdown
# Backend Development Guidelines

For backend development, use `uv` for dependency management.

Useful Commands

    # Sync dependencies from lockfile
    uv sync

    # Add a new package
    uv add <PACKAGE-NAME>

    # Run Python files
    uv run python <PYTHON-FILE>
```

**Note:** Some AI assistants (like Antigravity) may not automatically follow AGENTS.md.

You can explicitly ask them to follow these guidelines.

Also consider allowing automatic execution of commands starting with "uv" in your AI assistant preferences (File → Preferences → Antigravity Preferences).

### Step 5: Implement Backend with FastAPI

**Prompt for AI Assistant:**

```
based on the OpenAPI specs, create fastapi backend 
for now use a mock database, which we will later replace with a real one
create tests to make sure the implementation works

follow the guidelines in AGENTS.md
```

**Additional guidance:** Guide the AI to implement a `verify_api.py` script that tests the running server to ensure all endpoints work correctly.

---

## Integrating Frontend and Backend

### Connect Frontend to Backend API

**Prompt for AI Assistant:**

```
Now make frontend use backend. use OpenAPI specs for guidance
follow the guidelines in AGENTS.md
```

### Run Both Services Concurrently

**Prompt for AI Assistant:**

```
How can I run both frontend and backend at the same time? 
Let's use concurrently instead of our own script
```

### Debugging Issues

If something doesn't work (e.g., "Not Found" error on account creation):

**Prompt for AI Assistant:**

```
I tried creating an account and it says Not Found
write a test on backend to reproduce it, fix it, and make sure the frontend works fine too
```



## Adding Database Support

### Implement PostgreSQL/SQLite with SQLAlchemy

**Prompt for AI Assistant:**

```
now for backend let's use postgres and sqlite database (via sqlalchemy) 
follow the guidelines in AGENTS.md
```

### Add Integration Tests

After implementing the database layer:

**Prompt for AI Assistant:**

```
let's also add some integration tests (using sqlite) to make sure things work 
put the integration test in a separate folder tests_integration
```

---

## Containerization with Docker

### Create Docker Compose Setup

**Prompt for AI Assistant:**

```
right now we have frontend, backend, and database (sqlite)

let's put everything into docker compose and use postgres there. we can serve frontend with nginx or whatever you recommend
```

### Run with Docker Compose

```bash
# filepath: terminal
# Build and start all services
docker-compose up --build

# Stop all services (Ctrl+C or in another terminal)
docker-compose down
```



Don't forget to stop codespaces:


```bash
gh cs stop -c <CODESPACE_NAME>
```