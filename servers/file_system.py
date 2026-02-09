from mcp.server.fastmcp import FastMCP
import os

server = FastMCP("fileHandling", host="127.0.0.1", port=8003, stateless_http=True)

@server.tool(name="create_file", description="Create a new file with content")
async def create_file(filename: str, content: str) -> str:
    try:
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{filename}' created successfully."
    except Exception as e:
        return f"Error creating file: {e}"

@server.tool(name="update_file", description="Update (overwrite) an existing file")
async def update_file(filename: str, content: str) -> str:
    try:
        if not os.path.exists(filename):
            return f"File '{filename}' does not exist."

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{filename}' updated successfully."
    except Exception as e:
        return f"Error updating file: {e}"

@server.tool(name="read_file", description="Read the contents of a file")
async def read_file(filename: str) -> str:
    try:
        if not os.path.exists(filename):
            return f"File '{filename}' does not exist."

        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

@server.tool(name="list_files", description="List files and folders in a directory")
async def list_files(path: str = ".") -> str:
    try:
        if not os.path.isdir(path):
            return f"'{path}' is not a directory."

        items = os.listdir(path)
        if not items:
            return "Directory is empty."

        return "\n".join(items)
    except Exception as e:
        return f"Error listing files: {e}"

@server.tool(name="create_folder", description="Create a new folder")
async def create_folder(path: str) -> str:
    try:
        os.makedirs(path, exist_ok=True)
        return f"Folder '{path}' created successfully."
    except Exception as e:
        return f"Error creating folder: {e}"


@server.resource(
    name="file_system_capabilities",
    description="Read-only documentation describing file system capabilities and constraints",
    mime_type="text/plain"
)
async def file_system_capabilities() -> str:
    return """
File Handling MCP Server – Capabilities Reference

Available Tools:
- create_file(filename, content): Create a new file
- update_file(filename, content): Overwrite an existing file
- read_file(filename): Read file contents
- list_files(path): List files and folders in a directory
- create_folder(path): Create a directory

Behavior:
- Paths are resolved relative to the server's working directory.
- Files are treated as UTF-8 text.
- Existing files may be overwritten by update operations.

Constraints & Safety:
- File deletion is not supported.
- Binary files are not supported.
- Recursive directory listing is not supported.
- Access depends on server filesystem permissions.

Usage Notes:
- Use explicit paths when possible.
- Prefer creating folders before creating files within them.
- This resource is read-only and intended for contextual reference.
"""


@server.prompt(
    name="file_management_workflow",
    description="Guide the model to manage files and folders using file system tools"
)
async def file_management_workflow() -> str:
    return """
You are a file management assistant operating within an MCP server.

Your role:
- Interpret user requests related to file or folder operations.
- Select the correct file system tool.
- Execute the tool to perform the requested action.
- Return the tool output exactly as received.

Rules:
- Always use a tool to perform file system operations.
- Do NOT claim to read, write, or modify files without calling a tool.
- Perform only the action explicitly requested by the user.
- If required information is missing, ask for clarification.
- If an operation is unsupported or unsafe, refuse politely.

Tool selection guide:
- Create a file → create_file
- Update a file → update_file
- Read a file → read_file
- List directory contents → list_files
- Create a folder → create_folder

Output rules:
- Return only the tool result.
- Do not add explanations unless an error occurs.

This prompt ensures safe, transparent, and consistent file system operations.
"""
