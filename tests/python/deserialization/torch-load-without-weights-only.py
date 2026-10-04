import torch

# ruleid: torch-load-without-weights-only
state = torch.load("downloaded/model.pt")
# ruleid: torch-load-without-weights-only
state = torch.load(path, map_location="cpu", weights_only=False)
# ruleid: torch-load-without-weights-only
scripted = torch.jit.load("model.ts")

# ok: torch-load-without-weights-only
state = torch.load("downloaded/model.pt", weights_only=True)
# ok: torch-load-without-weights-only
state = torch.load(path, map_location="cpu", weights_only=True)
# ok: torch-load-without-weights-only
from safetensors.torch import load_file
tensors = load_file("model.safetensors")
