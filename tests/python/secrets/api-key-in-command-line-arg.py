import argparse
import os
import subprocess

parser = argparse.ArgumentParser()
# ruleid: api-key-in-command-line-arg
parser.add_argument("--api-key", required=True, help="provider API key")
# ruleid: api-key-in-command-line-arg
parser.add_argument("--openai-api-key")
# ruleid: api-key-in-command-line-arg
parser.add_argument("-k", "--anthropic_key", dest="key")
# ruleid: api-key-in-command-line-arg
parser.add_argument("--hf-token")
# ok: api-key-in-command-line-arg
parser.add_argument("--model", default="model-name")
# ok: api-key-in-command-line-arg
parser.add_argument("--max-tokens", type=int, default=256)
# ok: api-key-in-command-line-arg
parser.add_argument("--api-key-file", help="path to a file containing the key")

args = parser.parse_args()


def launch_worker(key: str):
    # ruleid: api-key-in-command-line-arg
    subprocess.run(["python", "worker.py", "--api-key", key])
    # ruleid: api-key-in-command-line-arg
    subprocess.Popen(["worker", f"--token={key}"])
    # ruleid: api-key-in-command-line-arg
    subprocess.run(["worker", "--key", os.environ["OPENAI_API_KEY"]])
    # ok: api-key-in-command-line-arg
    subprocess.run(["python", "worker.py"], env={**os.environ, "OPENAI_API_KEY": key})
    # ok: api-key-in-command-line-arg
    subprocess.run(["python", "worker.py", "--model", "model-name"])
