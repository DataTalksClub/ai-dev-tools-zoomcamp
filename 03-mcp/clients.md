# Configuration 

## GitHub Copilot 

...

## Codex
### CODEX + MCP Setup (VS Code — Linux)

> These steps assume a **Linux** environment. Paths and commands may differ on Windows or macOS.

#### 1. Install Codex Extension and Sign In
- Install **OpenAI Codex** from the VS Code Marketplace  
- Sign in with your OpenAI account

#### 2. Install the Codex CLI (Required)
Run in a terminal:
```bash
    npm install -g @openai/codex
    codex --version
```
Installing the CLI initializes the Codex config and `config.toml`.

#### 3. Open Codex MCP Settings
- Open the **Codex** tab in VS Code  
- Click the **Settings (⚙️)** button  
- This opens the `config.toml` file used by Codex

#### 4. Configure the MCP Server (Linux)
Add the following to `config.toml`:
```toml
    [codex.mcp_servers.hw3-mcp]
    command = "uv"
    args = [
      "--directory",
      "/path/to/ai-dev-tools-zoomcamp/03-mcp",
      "run",
      "python",
      "main.py"
    ]
    startup_timeout_sec = 10
    tool_timeout_sec = 60
    enabled = true
```
**Note on server name**  
`hw3-mcp` is just a configuration label. It can be renamed to anything meaningful (e.g. `local-mcp`, `mcp-tools`). The name only needs to be unique and does not need to match the project folder or any code.

### 5. Trust the Project
Also add:
```TOML
    [projects."/path/to/ai-dev-tools-zoomcamp"]
    trust_level = "trusted"
```
### 6. Expected Behavior
- MCP **tools** are available to Codex  
- If the server is tools-only, Codex will report **no MCP resources** (this is expected)


## Cursor 

...

## Antigravity 


...
