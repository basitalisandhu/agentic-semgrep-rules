import json
import pickle
import joblib
import numpy as np

# ruleid: pickle-load-model-file
model = pickle.load(open("downloads/classifier.pkl", "rb"))
# ruleid: pickle-load-model-file
embeddings = joblib.load("cache/embeddings.joblib")
# ruleid: pickle-load-model-file
memory = pickle.loads(blob)
# ruleid: pickle-load-model-file
arr = np.load("vectors.npy", allow_pickle=True)
# ruleid: pickle-load-model-file
model = AutoModelForCausalLM.from_pretrained("org/model", use_safetensors=False)

# ok: pickle-load-model-file
arr = np.load("vectors.npy")
# ok: pickle-load-model-file
memory = json.load(open("memory.json"))
# ok: pickle-load-model-file
from safetensors.torch import load_file
weights = load_file("model.safetensors")
# ok: pickle-load-model-file
pickle.dump(model, open("out.pkl", "wb"))
