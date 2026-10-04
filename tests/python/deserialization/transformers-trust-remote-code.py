from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# ruleid: transformers-trust-remote-code
model = AutoModelForCausalLM.from_pretrained("org/custom-model", trust_remote_code=True)
# ruleid: transformers-trust-remote-code
tok = AutoTokenizer.from_pretrained("org/custom-model", trust_remote_code=True, use_fast=True)
# ruleid: transformers-trust-remote-code
pipe = pipeline("text-generation", model="org/custom-model", trust_remote_code=True)
# ruleid: transformers-trust-remote-code
ds = load_dataset("org/custom-dataset", trust_remote_code=True)

# ok: transformers-trust-remote-code
safe_model = AutoModelForCausalLM.from_pretrained("org/model")
# ok: transformers-trust-remote-code
explicit = AutoModelForCausalLM.from_pretrained("org/model", trust_remote_code=False)
# ok: transformers-trust-remote-code
pinned = AutoModelForCausalLM.from_pretrained("org/custom-model", trust_remote_code=True, revision="7d3c2a1f9b8e4c6d5a0f1e2d3c4b5a69788796a5")
