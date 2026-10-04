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
