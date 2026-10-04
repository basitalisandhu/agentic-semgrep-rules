import os
from openai import OpenAI

# ruleid: hardcoded-llm-api-key
OPENAI_API_KEY = "sk-0123456789abcdefghijABCDEFGHIJ0123456789abcdefgh"
# ruleid: hardcoded-llm-api-key
client = OpenAI(api_key="sk-proj-0123456789abcdefghijABCDEFGHIJ0123456789abcdefghijklmnopqrstuvwxyz_ABCD")
# ruleid: hardcoded-llm-api-key
ANTHROPIC_API_KEY = "sk-ant-api03-0123456789abcdefghijABCDEFGHIJ0123456789abcdefghijklmnopqrstuvwxyzAA-0123456789AA"
# ruleid: hardcoded-llm-api-key
HF_TOKEN = "hf_0123456789abcdefghijABCDEFGHIJ0123"
# ruleid: hardcoded-llm-api-key
GROQ = "gsk_0123456789abcdefghijABCDEFGHIJ0123456789abcdefghij"
# ruleid: hardcoded-llm-api-key
GOOGLE = "AIza0123456789abcdefghijABCDEFGHIJ01234"

# ok: hardcoded-llm-api-key
key = os.environ["OPENAI_API_KEY"]
# ok: hardcoded-llm-api-key
client2 = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# ok: hardcoded-llm-api-key
placeholder = "sk-..."
# ok: hardcoded-llm-api-key
example = "sk-xxxxxxxxxxxxxxxxxxxx"
# ok: hardcoded-llm-api-key
prefix_check = api_key.startswith("sk-ant-")
# ok: hardcoded-llm-api-key
hf_prefix = token.startswith("hf_")
