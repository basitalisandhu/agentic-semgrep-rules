const childProcess = require("node:child_process");

module.exports = async function runFromModel(client, task) {
  const response = await client.responses.create({ input: task });
  const command = response.output_text;
  // ruleid: llm-output-to-child-process
  childProcess.exec(command);
  // ok: llm-output-to-child-process
  childProcess.execFile("echo", [command]);
};
