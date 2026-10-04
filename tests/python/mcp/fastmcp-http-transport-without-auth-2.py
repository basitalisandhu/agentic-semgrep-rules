from fastmcp import FastMCP
from fastmcp.server.auth import JWTVerifier

auth = JWTVerifier(jwks_uri="https://auth.example.com/.well-known/jwks.json", issuer="https://auth.example.com", audience="mcp")
mcp = FastMCP("demo", auth=auth)


@mcp.tool
def hello(name: str) -> str:
    return f"hello {name}"


if __name__ == "__main__":
    # ok: fastmcp-http-transport-without-auth
    mcp.run(transport="http", host="127.0.0.1", port=8000)
