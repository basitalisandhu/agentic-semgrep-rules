from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    # ruleid: fastmcp-http-transport-without-auth
    mcp.run(transport="sse")


def streamable():
    # ruleid: fastmcp-http-transport-without-auth
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)


def asgi():
    import uvicorn
    # ruleid: fastmcp-http-transport-without-auth
    uvicorn.run(mcp.sse_app(), host="127.0.0.1", port=8000)


secured = FastMCP("demo", token_verifier=MyTokenVerifier(), auth=AuthSettings(issuer_url="https://auth.example.com", resource_server_url="https://mcp.example.com"))


def secured_main():
    # ok: fastmcp-http-transport-without-auth
    secured.run(transport="streamable-http")


def stdio_main():
    # ok: fastmcp-http-transport-without-auth
    mcp.run(transport="stdio")
    # ok: fastmcp-http-transport-without-auth
    mcp.run()
