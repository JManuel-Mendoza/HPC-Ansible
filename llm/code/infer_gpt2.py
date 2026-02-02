import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed

CKPT = os.environ.get("CKPT", "/srv/nfs/llm-express/checkpoints/gpt2-tinystories-express/checkpoint-2000")

prompts = [
    "Once upon a time,",
    "The little robot said,",
    "In a small village, there was",
]

print("Checkpoint:", CKPT)
print("Torch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

device = "cuda" if torch.cuda.is_available() else "cpu"
set_seed(42)

tokenizer = AutoTokenizer.from_pretrained(CKPT, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(CKPT)
model.to(device)
model.eval()

gen_kwargs = dict(
    max_new_tokens=80,
    do_sample=True,
    temperature=0.9,
    top_p=0.95,
)

for i, p in enumerate(prompts, 1):
    inputs = tokenizer(p, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model.generate(**inputs, **gen_kwargs)
    text = tokenizer.decode(out[0], skip_special_tokens=True)
    print("\n" + "="*20 + f" SAMPLE {i} " + "="*20)
    print(text)
