import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({ name: "demo", version: "1.0.0" });
// ok: mcp-http-transport-without-auth
const transport = new StdioServerTransport();
await server.connect(transport);
