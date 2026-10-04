import os
import shutil
from pathlib import Path
from openai import OpenAI

client = OpenAI()
BASE = Path("/srv/agent/workspace").resolve()


def read_tool(task: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": task}])
    path = resp.choices[0].message.content
    # ruleid: llm-output-to-file-path
    with open(path) as f:
        return f.read()


def write_tool(task: str):
    resp = client.responses.create(model="model-name", input=task)
    target = resp.output_text
    # ruleid: llm-output-to-file-path
    with open(os.path.join("/srv/agent", target), "w") as f:
        f.write("done")
    # ruleid: llm-output-to-file-path
    shutil.rmtree(target)


def pathlib_tool(agent, task: str):
    name = agent.run(task)
    # ruleid: llm-output-to-file-path
    return Path(name).read_text()


def loader_tool(chain, task: str):
    from langchain_community.document_loaders import TextLoader
    chosen = chain.invoke({"task": task})
    # ruleid: llm-output-to-file-path
    return TextLoader(chosen).load()


def ok_contained(task: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": task}])
    candidate = (BASE / resp.choices[0].message.content).resolve()
    if not candidate.is_relative_to(BASE):
        raise ValueError("path escapes workspace")
    # ok: llm-output-to-file-path
    return candidate.read_text()


def ok_basename(task: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": task}])
    name = os.path.basename(resp.choices[0].message.content)
    # ok: llm-output-to-file-path
    with open(os.path.join(BASE, name)) as f:
        return f.read()


def ok_allowlist(task: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": task}])
    name = resp.choices[0].message.content
    if name not in {"readme.md", "notes.txt"}:
        raise ValueError("not allowed")
    # ok: llm-output-to-file-path
    with open(BASE / name) as f:
        return f.read()


def ok_model_output_is_content_not_path(task: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": task}])
    # ok: llm-output-to-file-path
    with open("/srv/agent/output.txt", "w") as f:
        f.write(resp.choices[0].message.content)
