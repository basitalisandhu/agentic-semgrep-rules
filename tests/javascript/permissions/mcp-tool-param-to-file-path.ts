import fs from "node:fs";
import path from "node:path";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { tool } from "ai";
import { z } from "zod";

const server = new McpServer({ name: "files", version: "1.0.0" });
const WORKSPACE = path.resolve("/srv/agent/workspace");

server.tool("read_file", { path: z.string() }, async ({ path: target }) => {
  // ruleid: mcp-tool-param-to-file-path
  const data = fs.readFileSync(target, "utf8");
  return { content: [{ type: "text", text: data }] };
});

server.registerTool("write_file", { inputSchema: { file: z.string(), content: z.string() } }, async ({ file, content }) => {
  // ruleid: mcp-tool-param-to-file-path
  await fs.promises.writeFile(path.join(WORKSPACE, file), content);
  return { content: [] };
});

server.tool("delete_file", { name: z.string() }, async (args) => {
  // ruleid: mcp-tool-param-to-file-path
  fs.rmSync(args.name);
  return { content: [] };
});

export const readTool = tool({
  description: "Read a file",
  parameters: z.object({ filePath: z.string() }),
  execute: async ({ filePath }) => {
    // ruleid: mcp-tool-param-to-file-path
    return fs.promises.readFile(filePath, "utf8");
  },
});

server.tool("read_contained", { path: z.string() }, async ({ path: target }) => {
  const resolved = path.resolve(WORKSPACE, target);
  if (!resolved.startsWith(WORKSPACE + path.sep)) {
    throw new Error("path escapes workspace");
  }
  // ok: mcp-tool-param-to-file-path
  const data = fs.readFileSync(resolved, "utf8");
  return { content: [{ type: "text", text: data }] };
});

server.tool("read_by_name", { name: z.string() }, async ({ name }) => {
  const safe = path.basename(name);
  // ok: mcp-tool-param-to-file-path
  const data = fs.readFileSync(path.join(WORKSPACE, safe), "utf8");
  return { content: [{ type: "text", text: data }] };
});

server.tool("read_allowlisted", { name: z.enum(["README.md", "CHANGELOG.md"]) }, async ({ name }) => {
  if (!["README.md", "CHANGELOG.md"].includes(name)) {
    throw new Error("not allowed");
  }
  // ok: mcp-tool-param-to-file-path
  const data = fs.readFileSync(path.join(WORKSPACE, name), "utf8");
  return { content: [{ type: "text", text: data }] };
});

server.tool("append_note", { text: z.string() }, async ({ text }) => {
  // ok: mcp-tool-param-to-file-path
  fs.appendFileSync(path.join(WORKSPACE, "notes.txt"), text);
  return { content: [] };
});
