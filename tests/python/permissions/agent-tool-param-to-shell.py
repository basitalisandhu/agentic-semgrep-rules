import asyncio
import os
import shlex
import subprocess
from mcp.server.fastmcp import FastMCP
from langchain_core.tools import tool
from agents import function_tool

mcp = FastMCP("ops")
ALLOWED = {"status", "log", "diff"}


@mcp.tool()
def run_command(command: str) -> str:
    """Run any shell command."""
    # ruleid: agent-tool-param-to-shell
    return subprocess.run(command, shell=True, capture_output=True, text=True).stdout


@mcp.tool()
async def run_async(cmd: str) -> str:
    # ruleid: agent-tool-param-to-shell
    proc = await asyncio.create_subprocess_shell(cmd)
    return str(proc)


@tool
def terminal(cmd: str) -> str:
    """Execute a terminal command."""
    # ruleid: agent-tool-param-to-shell
    return os.popen(cmd).read()


@function_tool
def shell(command: str) -> str:
    # ruleid: agent-tool-param-to-shell
    os.system(command)
    return "done"


@mcp.tool()
def git_subcommand(subcommand: str) -> str:
    if subcommand not in ALLOWED:
        raise ValueError("subcommand not allowed")
    # ok: agent-tool-param-to-shell
    return subprocess.run(["git", subcommand], capture_output=True, text=True, timeout=10).stdout


@mcp.tool()
def word_count(path: str) -> str:
    # ok: agent-tool-param-to-shell
    return subprocess.run(["wc", "-l", path], capture_output=True, text=True).stdout


@mcp.tool()
def say(text: str) -> str:
    # ok: agent-tool-param-to-shell
    return subprocess.run("say " + shlex.quote(text), shell=True).returncode


@mcp.tool()
def status() -> str:
    # ok: agent-tool-param-to-shell
    return subprocess.run("git status", shell=True, capture_output=True, text=True).stdout


def helper(command: str) -> str:
    # ok: agent-tool-param-to-shell
    return os.popen(command).read()
