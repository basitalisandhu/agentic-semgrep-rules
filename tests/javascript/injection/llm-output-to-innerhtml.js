const client = new OpenAI();

async function render(question) {
  const completion = await client.chat.completions.create({ model: "model-name", messages: [{ role: "user", content: question }] });
  const answer = completion.choices[0].message.content;
  // ruleid: llm-output-to-innerhtml
  document.getElementById("out").innerHTML = answer;
  // ruleid: llm-output-to-innerhtml
  out.insertAdjacentHTML("beforeend", marked.parse(answer));
  // ruleid: llm-output-to-innerhtml
  $("#out").html(answer);
  // ok: llm-output-to-innerhtml
  document.getElementById("out").textContent = answer;
  // ok: llm-output-to-innerhtml
  out.innerHTML = DOMPurify.sanitize(marked.parse(answer));
}

async function fromAnthropic(prompt) {
  const msg = await anthropic.messages.create({ model: "model-name", max_tokens: 256, messages: [{ role: "user", content: prompt }] });
  // ruleid: llm-output-to-innerhtml
  document.write(msg.content[0].text);
}

async function fromChain(chain, question) {
  const answer = await chain.invoke({ question });
  // ruleid: llm-output-to-innerhtml
  el.outerHTML = `<p>${answer}</p>`;
}
