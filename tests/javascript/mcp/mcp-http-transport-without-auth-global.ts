import express from "express";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { requireBearerAuth } from "@modelcontextprotocol/sdk/server/auth/middleware/bearerAuth.js";

const app = express();
app.use(express.json());
app.use(requireBearerAuth({ verifier, requiredScopes: ["mcp:tools"] }));

app.post("/mcp", async (req, res) => {
  // ok: mcp-http-transport-without-auth
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined,
    enableDnsRebindingProtection: true,
    allowedHosts: ["127.0.0.1"],
  });
  await transport.handleRequest(req, res, req.body);
});
