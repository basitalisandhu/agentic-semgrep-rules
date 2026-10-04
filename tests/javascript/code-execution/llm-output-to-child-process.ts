import { exec, execFile, spawn } from "node:child_process";
import OpenAI from "openai";

const client = new OpenAI();

export async function runFromModel(task: string) {
  const completion = await client.chat.completions.create({
    model: "model-name",
    messages: [{ role: "user", content: task }],
  });
  const cmd = completion.choices[0].message.content ?? "";
  // ruleid: llm-output-to-child-process
  exec(cmd);
  // ruleid: llm-output-to-child-process
  exec(`bash -lc "${cmd}"`, (err, stdout) => console.log(stdout));
  // ruleid: llm-output-to-child-process
  spawn("sh", ["-c", cmd], { shell: true });
  // ruleid: llm-output-to-child-process
  spawn(cmd, []);
  // ok: llm-output-to-child-process
  execFile("wc", ["-l", cmd]);
  // ok: llm-output-to-child-process
  spawn("echo", [cmd]);
}

export async function fromAiSdk(prompt: string) {
  const { text } = await generateText({ model: someModel, prompt });
  // ruleid: llm-output-to-child-process
  require("child_process").execSync(text);
}

export async function fromAgent(agentExecutor: any, question: string) {
  const result = await agentExecutor.invoke({ input: question });
  // ruleid: llm-output-to-child-process
  execFile(result.output, [], { shell: true });
}

export function fromParameter(response: any) {
  // ruleid: llm-output-to-child-process
  exec(response.choices[0].message.content);
}

export function okStatic() {
  // ok: llm-output-to-child-process
  exec("git status");
}

export async function okNumeric(task: string) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: task }] });
  const n = parseInt(completion.choices[0].message.content ?? "0", 10);
  // ok: llm-output-to-child-process
  exec(`sleep ${n}`);
}
