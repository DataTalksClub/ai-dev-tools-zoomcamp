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

### Prerequisites

- Antigravity AI Assistant (Google Deepmind)
- Node.js and npm installed (for most MCP servers)
- API keys for third-party MCP servers (if required)

### Configuration File Location

Antigravity reads MCP server configurations from a JSON file. The configuration file should be named `mcp.json` and placed in your project directory.

### Basic Configuration Format

Create an `mcp.json` file with the following structure:

```json
{
    "mcpServers": {
        "server-name": {
            "command": "command-to-run",
            "args": [
                "argument1",
                "argument2"
            ]
        }
    }
}
```

### Example: Adding Context7 MCP Server

Context7 provides access to library documentation and code search capabilities.

#### Step 1: Create mcp.json

```json
{
    "mcpServers": {
        "context7": {
            "command": "npx",
            "args": [
                "-y",
                "@upstash/context7-mcp@latest"
            ]
        }
    }
}
```

#### Step 2: Set Up API Key (if required)

Some MCP servers like Context7 require authentication:

**On Windows (PowerShell):**
```powershell
$env:CONTEXT7_API_KEY="your-api-key-here"
```

**On Linux/Mac:**
```bash
export CONTEXT7_API_KEY="your-api-key-here"
```

**Permanent Setup (Windows):**
Add to your PowerShell profile or set as system environment variable.

#### Step 3: Restart Antigravity

After adding the MCP configuration, restart Antigravity to load the new MCP server.

#### Step 4: Verify MCP Server Connection

Once Antigravity restarts, you can verify that your MCP server is connected:

1. **In Antigravity UI:** Click the **three dots (⋮)** menu in the interface
2. **Look for "MCP Servers"** or similar option that shows connected servers
3. You should see your configured server(s) listed (e.g., "context7")

> [!IMPORTANT]
> **If your MCP server doesn't appear:**
> - Verify the `mcp.json` file is in the correct location
> - Check for JSON syntax errors (use a JSON validator)
> - Ensure Node.js and npm are installed and accessible from command line
> - Check that the server package name is correct (e.g., `@upstash/context7-mcp@latest`)
> - Review Antigravity's logs for any error messages
> - Try running the MCP command manually in your terminal to test if it works:
>   ```powershell
>   npx -y @upstash/context7-mcp@latest
>   ```

> [!TIP]
> If Context7 or another server doesn't exist in your MCP servers list after following all steps:
> 1. Double-check your `mcp.json` syntax matches the examples exactly
> 2. Ensure you have an active internet connection (needed for `npx` to download packages)
> 3. Restart Antigravity completely (close and reopen the application)
> 4. Check if you need to set required environment variables (like `CONTEXT7_API_KEY`)


...
