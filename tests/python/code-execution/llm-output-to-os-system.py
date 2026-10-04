import os
import shlex
from anthropic import Anthropic

client = Anthropic()


def shell_from_model(task: str):
    msg = client.messages.create(model="model-name", max_tokens=512, messages=[{"role": "user", "content": task}])
    cmd = msg.content[0].text
    # ruleid: llm-output-to-os-system
    os.system(cmd)
    # ruleid: llm-output-to-os-system
    out = os.popen("sh -c " + cmd).read()
    # ruleid: llm-output-to-os-system
    os.execvp(cmd, [cmd])
    return out


def litellm_output(prompt: str):
    import litellm
    resp = litellm.completion(model="model-name", messages=[{"role": "user", "content": prompt}])
    # ruleid: llm-output-to-os-system
    os.system(f"echo {resp.choices[0].message.content} >> log.txt")


def from_parameter(response):
    # ruleid: llm-output-to-os-system
    os.popen(response.choices[0].message.content)


def ok_quoted(task: str):
    msg = client.messages.create(model="model-name", max_tokens=512, messages=[{"role": "user", "content": task}])
    # ok: llm-output-to-os-system
    os.system("say " + shlex.quote(msg.content[0].text))


def ok_static():
    # ok: llm-output-to-os-system
    os.system("clear")


def ok_output_only_logged(task: str):
    msg = client.messages.create(model="model-name", max_tokens=512, messages=[{"role": "user", "content": task}])
    # ok: llm-output-to-os-system
    print(msg.content[0].text)
