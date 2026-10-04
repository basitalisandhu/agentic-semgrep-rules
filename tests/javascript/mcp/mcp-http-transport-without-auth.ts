import express from "express";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { requireBearerAuth } from "@modelcontextprotocol/sdk/server/auth/middleware/bearerAuth.js";

const app = express();
app.use(express.json());
const server = new McpServer({ name: "demo", version: "1.0.0" });

app.post("/mcp", async (req, res) => {
  // ruleid: mcp-http-transport-without-auth
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});

app.get("/sse", async (req, res) => {
  // ruleid: mcp-http-transport-without-auth
  const transport = new SSEServerTransport("/messages", res);
  await server.connect(transport);
});

app.post("/mcp-protected", requireBearerAuth({ verifier, requiredScopes: ["mcp:tools"] }), async (req, res) => {
  // ok: mcp-http-transport-without-auth
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});

app.use("/mcp-session", sessionAuthMiddleware);
app.post("/mcp-session", async (req, res) => {
  // ok: mcp-http-transport-without-auth
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  await server.connect(transport);
});

app.listen(3000, "127.0.0.1");
