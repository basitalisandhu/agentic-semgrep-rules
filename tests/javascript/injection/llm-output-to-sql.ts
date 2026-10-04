import { Pool } from "pg";
import OpenAI from "openai";

const client = new OpenAI();
const pool = new Pool();

export async function textToSql(question: string) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: question }] });
  const sql = completion.choices[0].message.content ?? "";
  // ruleid: llm-output-to-sql
  const rows = await pool.query(sql);
  // ruleid: llm-output-to-sql
  await prisma.$queryRawUnsafe(`SELECT * FROM users WHERE name = '${sql}'`);
  // ruleid: llm-output-to-sql
  await knex.raw("SELECT * FROM t WHERE x = " + sql);
  return rows;
}

export async function fromChain(chain: any, question: string) {
  const generated = await chain.invoke({ question });
  // ruleid: llm-output-to-sql
  return sequelize.query(generated);
}

export async function okParameterised(question: string) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: question }] });
  const name = completion.choices[0].message.content ?? "";
  // ok: llm-output-to-sql
  await pool.query("SELECT * FROM users WHERE name = $1", [name]);
  // ok: llm-output-to-sql
  await prisma.$queryRaw`SELECT * FROM users WHERE name = ${name}`;
  // ok: llm-output-to-sql
  await knex("users").where({ name });
}

export async function okNumeric(question: string) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: question }] });
  const limit = parseInt(completion.choices[0].message.content ?? "10", 10);
  // ok: llm-output-to-sql
  await pool.query(`SELECT * FROM users LIMIT ${limit}`);
}

export async function okStatic() {
  // ok: llm-output-to-sql
  await pool.query("SELECT 1");
}
