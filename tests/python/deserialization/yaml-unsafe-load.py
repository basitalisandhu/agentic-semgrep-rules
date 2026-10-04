import yaml

with open("agent.yaml") as f:
    # ruleid: yaml-unsafe-load
    config = yaml.load(f)
# ruleid: yaml-unsafe-load
prompts = yaml.load(open("prompts.yaml"), Loader=yaml.Loader)
# ruleid: yaml-unsafe-load
skills = yaml.load(text, Loader=yaml.UnsafeLoader)
# ruleid: yaml-unsafe-load
tools = yaml.load(text, Loader=yaml.FullLoader)
# ruleid: yaml-unsafe-load
docs = yaml.unsafe_load(text)
# ruleid: yaml-unsafe-load
docs = yaml.full_load(text)

# ok: yaml-unsafe-load
config = yaml.safe_load(open("agent.yaml"))
# ok: yaml-unsafe-load
config = yaml.load(text, Loader=yaml.SafeLoader)
# ok: yaml-unsafe-load
config = yaml.load(text, Loader=yaml.CSafeLoader)
# ok: yaml-unsafe-load
docs = yaml.safe_load_all(text)
