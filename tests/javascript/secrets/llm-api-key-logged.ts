import "dotenv/config";
import pino from "pino";

const logger = pino();

// ruleid: llm-api-key-logged
console.log(process.env.OPENAI_API_KEY);
// ruleid: llm-api-key-logged
console.log(`anthropic key: ${process.env["ANTHROPIC_API_KEY"]}`);
// ruleid: llm-api-key-logged
logger.info({ token: process.env.HF_TOKEN }, "loaded token");
// ruleid: llm-api-key-logged
console.debug("env", process.env);
// ruleid: llm-api-key-logged
console.table(process.env);

const key = process.env.OPENAI_API_KEY;
// ruleid: llm-api-key-logged
logger.debug(`using key ${key}`);

// ok: llm-api-key-logged
console.log(process.env.NODE_ENV);
// ok: llm-api-key-logged
console.log("OPENAI_API_KEY set:", Boolean(process.env.OPENAI_API_KEY));
// ok: llm-api-key-logged
logger.info(`key suffix ...${key?.slice(-4)}`);
// ok: llm-api-key-logged
const client = new OpenAI({ apiKey: key });
// ok: llm-api-key-logged
console.log(process.env.OPENAI_API_KEY ? "set" : "missing");
