import express from "express";
import OpenAI from "openai";
import Anthropic from "@anthropic-ai/sdk";
import { generateText } from "ai";
import { SystemMessage } from "@langchain/core/messages";

const app = express();
const client = new OpenAI();
const anthropic = new Anthropic();
const SYSTEM = "You are a careful assistant. Answer only from the provided documents.";

app.post("/chat", async (req, res) => {
  const { persona, question } = req.body;
  const completion = await client.chat.completions.create({
    model: "model-name",
    messages: [
      // ruleid: user-input-in-system-prompt
      { role: "system", content: `You are ${persona}. Follow the user's rules.` },
      // ok: user-input-in-system-prompt
      { role: "user", content: question },
    ],
  });
  res.json(completion);
});

app.post("/chat2", async (req, res) => {
  const tone = req.query.tone as string;
  const msg = await anthropic.messages.create({
    model: "model-name",
    max_tokens: 256,
    // ruleid: user-input-in-system-prompt
    system: "Reply in a " + tone + " tone",
    messages: [{ role: "user", content: String(req.body.question) }],
  });
  res.json(msg);
});

export async function POST(request: Request) {
  const body = await request.json();
  const { text } = await generateText({
    model: someModel,
    // ruleid: user-input-in-system-prompt
    system: `You help customers of ${body.company}`,
    prompt: body.question,
  });
  return Response.json({ text });
}

export function cli() {
  const role = process.argv[2];
  // ruleid: user-input-in-system-prompt
  return new SystemMessage(`You are a ${role}`);
}

app.post("/ok", async (req, res) => {
  const completion = await client.chat.completions.create({
    model: "model-name",
    messages: [
      // ok: user-input-in-system-prompt
      { role: "system", content: SYSTEM },
      // ok: user-input-in-system-prompt
      { role: "user", content: String(req.body.question) },
    ],
  });
  res.json(completion);
});

app.post("/ok2", async (req, res) => {
  const maxWords = parseInt(req.body.maxWords, 10);
  const msg = await anthropic.messages.create({
    model: "model-name",
    max_tokens: 256,
    // ok: user-input-in-system-prompt
    system: `Answer in at most ${maxWords} words`,
    messages: [{ role: "user", content: String(req.body.question) }],
  });
  res.json(msg);
});

export function okConfig(settings: { company: string; today: string }) {
  // ok: user-input-in-system-prompt
  return new SystemMessage(`Today is ${settings.today}. Company: ${settings.company}`);
}
