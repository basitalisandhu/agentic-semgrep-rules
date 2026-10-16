import logging
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
logger = logging.getLogger(__name__)

# ruleid: llm-api-key-logged
print(os.environ["OPENAI_API_KEY"])
# ruleid: llm-api-key-logged
print("anthropic key:", os.getenv("ANTHROPIC_API_KEY"))
# ruleid: llm-api-key-logged
logger.info("using HF token %s", os.environ.get("HF_TOKEN"))
# ruleid: llm-api-key-logged
print(f"key={os.getenv('OPENAI_API_KEY')}")
# ruleid: llm-api-key-logged
print(os.environ)
# ruleid: llm-api-key-logged
print(dict(os.environ))
# ruleid: llm-api-key-logged
logging.debug("env: %s", dotenv_values(".env"))

key = os.environ.get("OPENAI_API_KEY")
# ruleid: llm-api-key-logged
logger.debug("loaded key %s", key)

# ok: llm-api-key-logged
print(os.getenv("MODEL_NAME"))
# ok: llm-api-key-logged
logger.info("OPENAI_API_KEY set: %s", bool(os.getenv("OPENAI_API_KEY")))
# ok: llm-api-key-logged
logger.info("key suffix ...%s", key[-4:])
# ok: llm-api-key-logged
client = OpenAI(api_key=key)
# ok: llm-api-key-logged
print(os.environ["HOME"])


def fetch_open_milestones(owner, repo, token):
    return http_get(f"https://api.github.com/repos/{owner}/{repo}/milestones", token=token)


token = os.environ.get("GITHUB_TOKEN")
milestones = fetch_open_milestones("o", "r", token)
# ok: llm-api-key-logged
print(milestones[0]["title"])

client = AsyncOpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))
agent = Agent(name="a", model=OpenAIChatCompletionsModel(model="m", openai_client=client))
result = Runner.run_sync(agent, "hi")
# ok: llm-api-key-logged
print(result.final_output)

# ruleid: llm-api-key-logged
print("key: {}".format(key))
# ruleid: llm-api-key-logged
print(str(key).strip())
