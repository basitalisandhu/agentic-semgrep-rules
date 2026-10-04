import DOMPurify from "dompurify";
import OpenAI from "openai";

const client = new OpenAI();

export async function Answer({ question }: { question: string }) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: question }] });
  const answer = completion.choices[0].message.content ?? "";
  // ruleid: llm-output-to-innerhtml
  return <div dangerouslySetInnerHTML={{ __html: answer }} />;
}

export async function SafeAnswer({ question }: { question: string }) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: question }] });
  const answer = completion.choices[0].message.content ?? "";
  // ok: llm-output-to-innerhtml
  return <div className="answer">{answer}</div>;
}

export async function SanitisedAnswer({ question }: { question: string }) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: question }] });
  const clean = DOMPurify.sanitize(completion.choices[0].message.content ?? "");
  // ok: llm-output-to-innerhtml
  return <div dangerouslySetInnerHTML={{ __html: clean }} />;
}
