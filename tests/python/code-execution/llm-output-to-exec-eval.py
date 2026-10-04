import ast
from openai import OpenAI
from anthropic import Anthropic

client = OpenAI()
anthropic = Anthropic()


def run_generated_code(task: str):
    resp = client.chat.completions.create(
        model="model-name", messages=[{"role": "user", "content": task}]
    )
    code = resp.choices[0].message.content
    # ruleid: llm-output-to-exec-eval
    exec(code)
    # ruleid: llm-output-to-exec-eval
    return eval(code.strip())


def responses_api(task: str):
    resp = client.responses.create(model="model-name", input=task)
    # ruleid: llm-output-to-exec-eval
    exec(resp.output_text)


def anthropic_sdk(task: str):
    msg = anthropic.messages.create(model="model-name", max_tokens=1024, messages=[{"role": "user", "content": task}])
    # ruleid: llm-output-to-exec-eval
    compile(msg.content[0].text, "<llm>", "exec")


def langchain_chain(chain, question: str):
    answer = chain.invoke({"question": question})
    # ruleid: llm-output-to-exec-eval
    return eval(answer["text"])


def agent_run(agent_executor, question: str):
    # ruleid: llm-output-to-exec-eval
    return eval(agent_executor.run(question))


def literal_eval_is_not_safe_either(response):
    # ruleid: llm-output-to-exec-eval
    return ast.literal_eval(response.choices[0].message.content)


def ok_parse_json(task: str):
    import json
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": task}])
    # ok: llm-output-to-exec-eval
    return json.loads(resp.choices[0].message.content)


def ok_static_code():
    code = "print('hello')"
    # ok: llm-output-to-exec-eval
    exec(code)


def ok_sandboxed(sandbox, task: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": task}])
    # ok: llm-output-to-exec-eval
    return sandbox.run_untrusted(resp.choices[0].message.content, timeout=5)


def ok_subprocess_result():
    import subprocess
    out = subprocess.run(["python", "-c", "print(1)"], capture_output=True, text=True).stdout
    # ok: llm-output-to-exec-eval
    return eval(out)
