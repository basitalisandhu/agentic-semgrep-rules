import uvicorn
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP

auth = AuthSettings(issuer_url="https://auth.example.com", resource_server_url="https://mcp.example.com")

# ruleid: fastmcp-bind-all-interfaces
mcp = FastMCP("files", host="0.0.0.0", port=8000, auth=auth, token_verifier=MyTokenVerifier())

# ok: fastmcp-bind-all-interfaces
local = FastMCP("files", host="127.0.0.1", port=8000, auth=auth, token_verifier=MyTokenVerifier())

# ok: fastmcp-bind-all-interfaces
default = FastMCP("files")


def main():
    # ruleid: fastmcp-bind-all-interfaces
    local.run(transport="sse", host="0.0.0.0", port=8000)


def settings():
    # ruleid: fastmcp-bind-all-interfaces
    local.settings.host = "0.0.0.0"


def asgi():
    # ruleid: fastmcp-bind-all-interfaces
    uvicorn.run(local.sse_app(), host="0.0.0.0", port=8000)
    # ok: fastmcp-bind-all-interfaces
    uvicorn.run(local.streamable_http_app(), host="127.0.0.1", port=8000)
    # ok: fastmcp-bind-all-interfaces
    local.run(transport="stdio")
