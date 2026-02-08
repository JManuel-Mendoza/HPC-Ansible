import argparse
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_dir", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--max_new_tokens", type=int, default=80)
    args = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(args.model_dir, use_fast=True)
    mdl = AutoModelForCausalLM.from_pretrained(args.model_dir)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    mdl.to(device)

    inp = tok(args.prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        out = mdl.generate(
            **inp,
            max_new_tokens=args.max_new_tokens,
            do_sample=True,
            temperature=0.8,
            top_p=0.95,
        )
    print(tok.decode(out[0], skip_special_tokens=True))

if __name__ == "__main__":
    main()
