# Module 3 — MCP Deep Dive & Agents (Developer-Centric Servers)

Videos:

* [▶️ Watch the Workshop Video](https://www.youtube.com/watch?v=0IhZdcjddo4&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)
* [Working Demo](https://www.youtube.com/watch?v=HYHv_S141CU&list=PL3MmuxUbc_hLuyafXPyhTdbF4s_uNhc43)

> Note: during the live stream we had some problems with the demo. Check the "Demo" for the working version.

## Overview

### All about MCP

- What is MCP and how it connects AI tools, servers, and clients
- How to use MCP primitives like tools, resources, and prompts
- Comparing MCP communication modes: stdio vs HTTPS

## Using MCP servers for developer workflows

- Using Context 7 for live documentation and debugging (Airflow, Astro)
- Configuring VSCode with MCP servers
- Automating workflows code fixing with latest docs
- Generating and writing blog posts to hashnode on the fly


## Demo Flow


### Part 1: Intro to MCP

#### 1. Clone the demo code repo

[Clone this repo - https://github.com/thelearningdev/mcp-ai-dev-workflow](https://github.com/thelearningdev/mcp-ai-dev-workflow)

#### 2. Setting up Python Environment

Ensure you have python 3.12+ installed

```
cd code
uv sync
uv venv
source .venv/bin/activate
```

#### 3. Play with your server

With your virtual env activated run...

```
cd 0-mcp-demo/stdio/
python stdio_server.py
```
The terminal will say `starting server` 

Now paste your JSON-RPC requests line by line

1. Initialize the client

```
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test-client","version":"1.0.0"}}}
```

2. initialize the notification

```
{"jsonrpc":"2.0","method":"notifications/initialized"}
```

> Note: You won't receive a JSON response here

3. list the tools

```
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
```

4. call the tool get weather

```
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_weather","arguments":{"city":"London"}}}
```

Congratulations 🎉 you have successfully called your first MCP tool in stdio mode.

#### 4. Let's visualize these features in MCP inspector

**1. Install `mcp-inspector`**

```
npx @modelcontextprotocol/inspector
```

If you do not have node installed, use brew installation

```
brew install mcp-inspector
mcp-inspector
```

On the MCP inspector that opens on your browser `http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=<some-token-here>`  


**2. Note down two things**

- Your python environment  
    - On your terminal Type `which python`you will get an answer like this `<YOUR_BASE_PATH>/mcp-for-ai-dev-course/code/.venv/bin/python` 
- Path to the `stdio_server.py`
    - On vscode, Right click on the `stdio_server.py` file and copy path `<YOUR_BASE_PATH>/mcp-for-ai-dev-course/code/0-mcp-demo/stdio/stdio_client.py` 

> Replace `YOUR_BASE_PATH` with right path according to your laptop

**3. Add these to MCP inspector**

1. Under command - add python path
2. Under Arguments - add stdio_server.py file path

> Note: You can also run

```
npx @modelcontextprotocol/inspector <command> <server_file_path>
```
---

```
npx @modelcontextprotocol/inspector \
  <YOUR_BASE_PATH>/mcp-for-ai-dev-course/code/.venv/bin/python \
  <YOUR_BASE_PATH>/mcp-for-ai-dev-course/code/0-mcp-demo/stdio/stdio_server.py
```

You can also run the server in http mode and link it to the inspector

---

### Part 2: MCP on AI Dev workflow

> You need Vscode + github copilot (free version should do) for this demo

1. Create an account in [context7](https://context7.com/) and copy your API Key, keep it aside

> We are not affiliated with context7, just a tool that works well

![alt text](../images/mcp/context7-apikey.png)

2. Under libraries tab in context7, pick the libraries of your choice

![alt text](../images/mcp/context7-libraries.png)

3. In the MCP inspector add the mcp url and explore the tools in HTTP mode.

![alt text](../images/mcp/mcp-inspector-with-context7.png)

4. In VScode install mcp servers using the extensions or using `mcp.json` file

### Write Code

1. Pick a library of your choice (something that you know really well). I've picked Airflow in the demo
2. You can use [Airflow Quickstart](https://airflow.apache.org/docs/apache-airflow/3.0.6/start.html) to quickly replicate the environment in the demo
3. Disable context7 and ask it to write code
4. Enable context7 and ask it to `use the latest docs` to fix the code written. 
5. Try different MCP servers like github to raise a PR, hashnode to publish a blog post, notion to capture notes
6. You can find some cool [MCP servers in this directory](https://github.com/mcp?utm_source=vscode-website&utm_campaign=mcp-registry-server-launch-2025)

## Relevant Links

- [Model Context Protocol — Site](https://modelcontextprotocol.io/)
- [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol)
- [TheLearningDev - Demo Repo](https://github.com/thelearningdev/mcp-ai-dev-workflow)
- [Using MCP servers in VScode](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)