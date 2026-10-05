import { exec, execFile } from "node:child_process";

export async function runFromModel(client, task) {
  const response = await client.responses.create({ input: task });
  const command = response.output_text;
  // ruleid: llm-output-to-child-process
  exec(command);
  // ok: llm-output-to-child-process
  execFile("echo", [command]);
}
