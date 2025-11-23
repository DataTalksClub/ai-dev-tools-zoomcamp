connecting antigravity to codepaces

- install github cli (download from here: https://github.com/cli/cli/releases)
- authenticate:
    - gh auth login
    - ssh protocol
    - select the ssh key you use for github 
    - follow the rest of the instructions
- authenticate for codespaces
    - run `gh codespace list` to see if you need it
    - `gh auth refresh -h github.com -s codespace`
- use codespaces:
    - `gh codespace create` for the repo we exported with lovable
    - note the id (`expert-doodle-wr7wg9p5gqcgggw`)
- connect using ssh:
    - `gh codespace ssh` 
    - get config: `gh codespace ssh --config -c expert-doodle-wr7wg9p5gqcgggw`
    - add it to `~/.ssh/config`
    - if you have an error "cannot find the key", create it `codespaces.auto`: `ssh-keygen -t ed25519 -f ~/.ssh/codespaces.auto`
    - test with `ssh <name>` that you can connect to it
- connect to it using antigravity's ssh remove mode
- open the project folder in `/workspaces/`
- stop when done
    - `gh cs stop -c expert-doodle-wr7wg9p5gqcgggw`




lovable prompt: 

```
create the snake game with two models: pass-through and walls. prepare to make it multiplayers - we will have this functionality: leaderboard and watching (me following other players that currently play). add mockups for that and also for log in.
everything should be interactive - I can log in, sign up, see my username when I'm logged in, see leaderboard, see
other people play (in this case just implement some playing logic yourself as if somebody is playing) 
make sure that all the logic is covered with tests 

don't implement backend, so everything is mocked. But centralize all the calls to the backend in one place
```


running it locally

- run it
- run tests
- run application


creating backend

now let's create a folder "frontend" and move all the files there

mkdir frontend
mv * frontend

todo: why OpenAPI

prmopt: analyse the content of the client and create an OpenAPI specs based on what it needs. later we want to implement backend based on these specs

now initialize the backend project 

pip install uv

mkdir backend
cd backend
uv init

create AGENTS.md

```
for backend, use uv for dependency management. a few useful commands:

uv sync
uv add <PACKAGE-NAME>
uv run python <PYTHON-FILE> 
```

Antigravity doesn't seem to follow the instructions there (but Cursor, Copilot, Codex, and many others do). You can ask it explicitly to follow the instruction there.

it's also a bit annoying to manually verity all the commands it tries to run, so let's allow it to run everything that starts with "uv". For antigravity it's file -> preferecens -> antrigravity preferences. In other assistants it's similar. In Github Copilot you can allow that when it runs for the first time.


Let's implement backend 

Prompt: 

```
based on the OpenAPI specs, create fastapi backend 
for now use a mock database, which we will later replace with a real one
create tests to make sure the implementation works

follow the guidelines in AGENTS.md
```

This is annoying so I hope google fixes it soon 

After that guide it until it produces a working implementation. You can ask it to
implement a "verify_api.py" that tests a working server. 



Putting everything togeter 

now we have frontend and backend. we also have API specs that define how they interact
let's now make them work together


prompt 

Now make frontend use backend. use OpenAPI specs for guidance


another prompt: 

How can I run both frontend and backend at the same time? 

Let's use concurrently instead of our own script


When somethng dosen't work:

```
I tried creating an account and it says Not Found
write a test on backend to reproduce it, fix it, and make sure the frontend works fine too
```

database

prompt: 

```
now for backend let's use postres and sqlite database (via sqlalchemy) 
```

After some time we may want to add tests:

```
let's also add some integration tests (using sqlite) to make sure things work 
put the integration test in a separate folder tests_integration
```


containerization


prompt 

right now we have front end back end and database (sqlite)

let's put everuthing into docker compose and use postgres there. we can serve frontend with nginx or whatever you recommend 

run it:

docker-compose up --build
