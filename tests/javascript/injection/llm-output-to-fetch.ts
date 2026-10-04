import axios from "axios";
import OpenAI from "openai";

const client = new OpenAI();

export async function browseTool(task: string) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: task }] });
  const url = completion.choices[0].message.content ?? "";
  // ruleid: llm-output-to-fetch
  const res = await fetch(url);
  // ruleid: llm-output-to-fetch
  const res2 = await axios.get(url, { timeout: 5000 });
  // ruleid: llm-output-to-fetch
  const res3 = await axios(`${url}/api`);
  return [res, res2, res3];
}

export async function fromAiSdk(prompt: string) {
  const { text } = await generateText({ model: someModel, prompt });
  // ruleid: llm-output-to-fetch
  await page.goto(text);
}

export async function fromAgent(agent: any, question: string) {
  const result = await agent.invoke({ input: question });
  // ruleid: llm-output-to-fetch
  return got(result.output).json();
}

export async function okFixedHost(task: string) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: task }] });
  const q = completion.choices[0].message.content ?? "";
  // ok: llm-output-to-fetch
  return fetch(`https://api.example.com/search?q=${encodeURIComponent(q)}`);
}

export async function okValidated(task: string) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: task }] });
  const safe = validateUrl(completion.choices[0].message.content ?? "", { allowHosts: ["docs.example.com"] });
  // ok: llm-output-to-fetch
  return fetch(safe, { redirect: "manual" });
}

export async function okStatic() {
  // ok: llm-output-to-fetch
  return fetch("https://example.com/health");
}
