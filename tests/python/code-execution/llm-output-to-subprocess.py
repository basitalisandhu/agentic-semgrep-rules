import shlex
import subprocess
from openai import OpenAI

client = OpenAI()


def ask(task: str) -> str:
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": task}])
    return resp.choices[0].message.content


def run_command_from_model(task: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": task}])
    cmd = resp.choices[0].message.content
    # ruleid: llm-output-to-subprocess
    subprocess.run(cmd, shell=True)
    # ruleid: llm-output-to-subprocess
    subprocess.check_output(f"bash -lc {cmd}", shell=True)
    # ruleid: llm-output-to-subprocess
    subprocess.Popen("sh -c " + cmd, shell=True, stdout=subprocess.PIPE)
    # ruleid: llm-output-to-subprocess
    subprocess.getoutput(cmd)
    # ruleid: llm-output-to-subprocess
    subprocess.run(cmd)


def ollama_tool(prompt: str):
    import ollama
    response = ollama.chat(model="model-name", messages=[{"role": "user", "content": prompt}])
    # ruleid: llm-output-to-subprocess
    subprocess.call(response["message"]["content"], shell=True)


def agent_output(agent, question: str):
    result = agent.invoke({"input": question})
    # ruleid: llm-output-to-subprocess
    subprocess.run(result["output"], shell=True)


def ok_fixed_program_with_list_args(task: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": task}])
    filename = resp.choices[0].message.content
    # ok: llm-output-to-subprocess
    subprocess.run(["wc", "-l", filename], check=True, timeout=5)


def ok_quoted(task: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": task}])
    arg = resp.choices[0].message.content
    # ok: llm-output-to-subprocess
    subprocess.run("ls " + shlex.quote(arg), shell=True)


def ok_static_command():
    # ok: llm-output-to-subprocess
    subprocess.run("ls -la", shell=True)


def ok_numeric(task: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": task}])
    seconds = int(resp.choices[0].message.content)
    # ok: llm-output-to-subprocess
    subprocess.run(f"sleep {seconds}", shell=True)
