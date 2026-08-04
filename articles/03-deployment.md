
The backend prompt asks Codex to add tests. A dedicated integration-test suite
does not appear in this session, so treat it as a follow-up once the SQLite
version works.

## Containers

We want one image with the backend and the compiled frontend, so there's a
single thing to build, run, and ship:

```text
Create a Dockerfile that builds the frontend with Node, then builds a Python
image with backend with frontend static files. Backend should serve the frontend.
```

The first image did not work because the frontend build did not produce the
static files the backend expected. Ask the assistant to look at the generated
frontend setup, adjust the build, and test the running container through its
public port.

You do not need to know every frontend build tool in advance. You do need to
test the generated artifact and give the assistant the observed failure.
