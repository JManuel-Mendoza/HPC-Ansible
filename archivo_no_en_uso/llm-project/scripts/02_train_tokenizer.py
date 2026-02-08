import argparse
from pathlib import Path
from tokenizers import ByteLevelBPETokenizer

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_dir", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--vocab_size", type=int, default=32000)
    ap.add_argument("--min_frequency", type=int, default=2)
    args = ap.parse_args()

    input_dir = Path(args.input_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = [str(input_dir / "train.txt"), str(input_dir / "val.txt")]
    for f in files:
        if not Path(f).exists():
            raise SystemExit(f"Falta archivo: {f}")

    tok = ByteLevelBPETokenizer()
    tok.train(
        files=files,
        vocab_size=args.vocab_size,
        min_frequency=args.min_frequency,
        special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>"],
    )
    tok.save_model(str(out_dir))
    print("OK ->", str(out_dir))

if __name__ == "__main__":
    main()
