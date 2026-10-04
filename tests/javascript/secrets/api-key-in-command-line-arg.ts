import { spawn } from "node:child_process";
import { Command } from "commander";
import OpenAI from "openai";

const program = new Command();
// ruleid: api-key-in-command-line-arg
program.option("--api-key <key>", "provider API key");
// ruleid: api-key-in-command-line-arg
program.requiredOption("--openai-api-key <key>");
// ruleid: api-key-in-command-line-arg
program.option("-k, --anthropic-key <key>", "key");
// ruleid: api-key-in-command-line-arg
yargs.option("hf-token", { type: "string" });
// ok: api-key-in-command-line-arg
program.option("--model <name>", "model name");
// ok: api-key-in-command-line-arg
program.option("--api-key-file <path>", "file containing the key");
// ok: api-key-in-command-line-arg
program.option("--max-tokens <n>");

// ruleid: api-key-in-command-line-arg
const client = new OpenAI({ apiKey: process.argv[2] });
// ok: api-key-in-command-line-arg
const client2 = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export function launchWorker(key: string) {
  // ruleid: api-key-in-command-line-arg
  spawn("node", ["worker.js", "--api-key", key]);
  // ruleid: api-key-in-command-line-arg
  spawn("worker", [`--token=${key}`]);
  // ruleid: api-key-in-command-line-arg
  spawn("worker", ["--key", process.env.OPENAI_API_KEY]);
  // ok: api-key-in-command-line-arg
  spawn("node", ["worker.js"], { env: { ...process.env, OPENAI_API_KEY: key } });
  // ok: api-key-in-command-line-arg
  spawn("node", ["worker.js", "--model", "model-name"]);
}
