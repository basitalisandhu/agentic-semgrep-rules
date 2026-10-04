import fs from "node:fs";
import path from "node:path";
import OpenAI from "openai";

const client = new OpenAI();
const WORKSPACE = path.resolve("/srv/agent/workspace");

export async function readTool(task: string) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: task }] });
  const target = completion.choices[0].message.content ?? "";
  // ruleid: llm-output-to-file-path
  const data = fs.readFileSync(target, "utf8");
  // ruleid: llm-output-to-file-path
  await fs.promises.writeFile(path.join(WORKSPACE, target), "done");
  // ruleid: llm-output-to-file-path
  fs.rmSync(target, { recursive: true });
  return data;
}

export async function fromAiSdk(prompt: string) {
  const { text } = await generateText({ model: someModel, prompt });
  // ruleid: llm-output-to-file-path
  return Bun.file(text).text();
}

export async function fromAgent(agent: any, question: string) {
  const result = await agent.invoke({ input: question });
  // ruleid: llm-output-to-file-path
  return new TextLoader(result.output).load();
}

export async function okContained(task: string) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: task }] });
  const resolved = path.resolve(WORKSPACE, completion.choices[0].message.content ?? "");
  if (!resolved.startsWith(WORKSPACE + path.sep)) {
    throw new Error("path escapes workspace");
  }
  // ok: llm-output-to-file-path
  return fs.promises.readFile(resolved, "utf8");
}

export async function okBasename(task: string) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: task }] });
  const name = path.basename(completion.choices[0].message.content ?? "");
  // ok: llm-output-to-file-path
  return fs.readFileSync(path.join(WORKSPACE, name), "utf8");
}

export async function okAllowlist(task: string) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: task }] });
  const name = completion.choices[0].message.content ?? "";
  if (!["README.md", "CHANGELOG.md"].includes(name)) {
    throw new Error("not allowed");
  }
  // ok: llm-output-to-file-path
  return fs.readFileSync(path.join(WORKSPACE, name), "utf8");
}

export async function okOutputIsContent(task: string) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: task }] });
  // ok: llm-output-to-file-path
  fs.writeFileSync(path.join(WORKSPACE, "answer.txt"), completion.choices[0].message.content ?? "");
}
