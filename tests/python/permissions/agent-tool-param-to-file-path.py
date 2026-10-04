import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from langchain_core.tools import tool

mcp = FastMCP("files")
WORKSPACE = Path("/srv/agent/workspace").resolve()


@mcp.tool()
def read_file(path: str) -> str:
    """Read any file."""
    # ruleid: agent-tool-param-to-file-path
    with open(path) as f:
        return f.read()


@mcp.tool()
def write_file(path: str, content: str) -> str:
    # ruleid: agent-tool-param-to-file-path
    Path(path).write_text(content)
    return "ok"


@mcp.tool()
async def delete_file(filename: str) -> str:
    # ruleid: agent-tool-param-to-file-path
    os.remove(os.path.join("/srv/agent/workspace", filename))
    return "deleted"


@tool
def list_dir(directory: str) -> list[str]:
    """List a directory."""
    # ruleid: agent-tool-param-to-file-path
    return os.listdir(directory)


@mcp.tool()
def read_contained(path: str) -> str:
    target = (WORKSPACE / path).resolve()
    if not target.is_relative_to(WORKSPACE):
        raise ValueError("path escapes workspace")
    # ok: agent-tool-param-to-file-path
    return target.read_text()


@mcp.tool()
def read_by_name(name: str) -> str:
    safe = os.path.basename(name)
    # ok: agent-tool-param-to-file-path
    with open(WORKSPACE / safe) as f:
        return f.read()


@mcp.tool()
def read_allowlisted(name: str) -> str:
    if name not in {"README.md", "CHANGELOG.md"}:
        raise ValueError("not allowed")
    # ok: agent-tool-param-to-file-path
    return (WORKSPACE / name).read_text()


@mcp.tool()
def read_checked(path: str) -> str:
    full = os.path.realpath(os.path.join(str(WORKSPACE), path))
    if not full.startswith(str(WORKSPACE)):
        raise ValueError("outside workspace")
    # ok: agent-tool-param-to-file-path
    with open(full) as f:
        return f.read()


@mcp.tool()
def append_note(text: str) -> str:
    # ok: agent-tool-param-to-file-path
    with open(WORKSPACE / "notes.txt", "a") as f:
        f.write(text)
    return "ok"
