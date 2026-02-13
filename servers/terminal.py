from mcp.server.fastmcp import FastMCP
import subprocess
import os

server = FastMCP("myTerminal", host="127.0.0.1", port=8002, stateless_http=True)

@server.tool(name="terminal", description="Run a terminal command")
async def terminal(command: str) -> str:
    try:
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        return output.stdout
    except Exception as e:
        return f"Error: {e}"

@server.resource(uri="terminal://terminal_capabilities",name="terminal_capabilities", description="Read-only documentation describing terminal capabilities and constraints")
async def terminal_capabilities() -> str:
    return """
Terminal MCP Server – Capabilities Reference

Overview:
This server provides controlled access to a system shell for executing terminal commands.

Available Tool:
- terminal(command: string)
  Executes a shell command and returns the standard output.

Execution Behavior:
- Commands are executed in the server's runtime environment.
- Output includes stdout only.
- stderr is not returned unless explicitly captured in the command.

Constraints & Safety:
- Commands should be read-only whenever possible.
- Avoid destructive commands (e.g., rm -rf, shutdown, reboot).
- Avoid long-running or blocking processes.
- Avoid commands requiring interactive input.
- Environment variables and filesystem access depend on server permissions.

Usage Notes:
- Each command should be self-contained.
- Prefer explicit flags and non-interactive modes.
- This resource is read-only and intended for contextual reference only.
"""

@server.prompt(name="terminal_workflow", description= "Guide the model to run terminal commands")
async def terminal_workflow() -> str:
    return """
You are a terminal assistant operating within an MCP server.

Your role:
- Interpret user requests related to terminal or system operations.
- Translate requests into safe, non-interactive shell commands.
- Execute commands using the terminal tool.
- Return the tool output exactly as received.

Rules:
- Always use the terminal tool to execute commands.
- Do NOT simulate or guess command output.
- Do NOT run destructive or irreversible commands.
- Do NOT run interactive commands.
- If a request is ambiguous, ask for clarification before execution.
- If a request is unsafe or unsupported, explain why and refuse politely.

Command guidelines:
- Prefer read-only commands (ls, cat, pwd, whoami, df, ps).
- Use explicit flags to avoid prompts.
- Keep commands short and focused.
- Execute one command at a time.

Output rules:
- Return only the command output.
- Do not add explanations unless the command fails.
- If an error occurs, return the error message.

This prompt ensures safe, transparent, and predictable terminal tool usage
"""

if __name__ == "__main__":
    server.run(transport="streamable-http")