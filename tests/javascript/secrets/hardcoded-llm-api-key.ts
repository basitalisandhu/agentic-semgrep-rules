import OpenAI from "openai";

// ruleid: hardcoded-llm-api-key
const OPENAI_API_KEY = "sk-0123456789abcdefghijABCDEFGHIJ0123456789abcdefgh";
// ruleid: hardcoded-llm-api-key
const client = new OpenAI({ apiKey: "sk-proj-0123456789abcdefghijABCDEFGHIJ0123456789abcdefghijklmnopqrstuvwxyz_ABCD" });
// ruleid: hardcoded-llm-api-key
const anthropicKey = `sk-ant-api03-0123456789abcdefghijABCDEFGHIJ0123456789abcdefghijklmnopqrstuvwxyzAA-0123456789AA`;
// ruleid: hardcoded-llm-api-key
const hfToken = 'hf_0123456789abcdefghijABCDEFGHIJ0123';
// ruleid: hardcoded-llm-api-key
const groq = "gsk_0123456789abcdefghijABCDEFGHIJ0123456789abcdefghij";

// ok: hardcoded-llm-api-key
const fromEnv = process.env.OPENAI_API_KEY;
// ok: hardcoded-llm-api-key
const client2 = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
// ok: hardcoded-llm-api-key
const placeholder = "sk-...";
// ok: hardcoded-llm-api-key
const example = "sk-xxxxxxxxxxxxxxxxxxxx";
// ok: hardcoded-llm-api-key
const isAnthropic = key.startsWith("sk-ant-");
