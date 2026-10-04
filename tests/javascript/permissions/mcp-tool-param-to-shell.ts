import { exec, execFile, spawn } from "node:child_process";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({ name: "ops", version: "1.0.0" });
const ALLOWED = ["status", "log", "diff"];

server.tool("run_command", { command: z.string() }, async ({ command }) => {
  // ruleid: mcp-tool-param-to-shell
  const out = execSync(command).toString();
  return { content: [{ type: "text", text: out }] };
});

server.registerTool(
  "shell",
  { description: "Run a shell command", inputSchema: { cmd: z.string() } },
  async ({ cmd }) => {
    // ruleid: mcp-tool-param-to-shell
    exec(`bash -lc "${cmd}"`);
    return { content: [] };
  }
);

server.tool("run_args", { args: z.array(z.string()) }, async (input) => {
  // ruleid: mcp-tool-param-to-shell
  spawn("sh", input.args, { shell: true });
  return { content: [] };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  // ruleid: mcp-tool-param-to-shell
  exec(request.params.arguments.command);
  return { content: [] };
});

server.tool("git", { subcommand: z.string() }, async ({ subcommand }) => {
  if (!ALLOWED.includes(subcommand)) {
    throw new Error("subcommand not allowed");
  }
  // ok: mcp-tool-param-to-shell
  const out = execFileSync("git", [subcommand]).toString();
  return { content: [{ type: "text", text: out }] };
});

server.tool("word_count", { path: z.string() }, async ({ path }) => {
  // ok: mcp-tool-param-to-shell
  execFile("wc", ["-l", path]);
  return { content: [] };
});

server.tool("status", {}, async () => {
  // ok: mcp-tool-param-to-shell
  const out = execSync("git status").toString();
  return { content: [{ type: "text", text: out }] };
});

export function helper(command: string) {
  // ok: mcp-tool-param-to-shell
  return execSync(command);
}
