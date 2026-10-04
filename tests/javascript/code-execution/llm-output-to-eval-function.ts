import vm from "node:vm";
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

export async function runGenerated(task: string) {
  const msg = await anthropic.messages.create({
    model: "model-name",
    max_tokens: 1024,
    messages: [{ role: "user", content: task }],
  });
  const code = msg.content[0].type === "text" ? msg.content[0].text : "";
  // ruleid: llm-output-to-eval-function
  eval(code);
  // ruleid: llm-output-to-eval-function
  const fn = new Function("input", code);
  // ruleid: llm-output-to-eval-function
  vm.runInNewContext(code, { console });
  // ruleid: llm-output-to-eval-function
  new vm.Script(code).runInThisContext();
  return fn;
}

export async function fromChain(chain: any, question: string) {
  const answer = await chain.invoke({ question });
  // ruleid: llm-output-to-eval-function
  return vm.runInContext(answer, vm.createContext({}));
}

export async function okJsonParse(task: string) {
  const msg = await anthropic.messages.create({ model: "model-name", max_tokens: 256, messages: [{ role: "user", content: task }] });
  // ok: llm-output-to-eval-function
  return JSON.parse(msg.content[0].text);
}

export function okStatic() {
  // ok: llm-output-to-eval-function
  return eval("1 + 1");
}

export async function okIsolated(sandbox: any, task: string) {
  const msg = await anthropic.messages.create({ model: "model-name", max_tokens: 256, messages: [{ role: "user", content: task }] });
  // ok: llm-output-to-eval-function
  return sandbox.runUntrusted(msg.content[0].text, { timeoutMs: 1000 });
}
