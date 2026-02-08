import argparse
import random
from pathlib import Path

def read_all_txt(raw_dir: Path) -> list[str]:
    texts = []
    for p in sorted(raw_dir.glob("*.txt")):
        with p.open("r", encoding="utf-8", errors="ignore") as f:
            t = f.read().strip()
            if t:
                texts.append(t)
    return texts

def normalize(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines).strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw_dir", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--val_ratio", type=float, default=0.02)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    raw_dir = Path(args.raw_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    texts = read_all_txt(raw_dir)
    if not texts:
        raise SystemExit(f"No se encontraron .txt en {raw_dir}")

    rng = random.Random(args.seed)
    rng.shuffle(texts)

    n_val = max(1, int(len(texts) * args.val_ratio))
    val = texts[:n_val]
    train = texts[n_val:]

    (out_dir / "train.txt").write_text("\n\n".join(normalize(t) for t in train) + "\n", encoding="utf-8")
    (out_dir / "val.txt").write_text("\n\n".join(normalize(t) for t in val) + "\n", encoding="utf-8")

    print("OK")
    print("train_docs:", len(train))
    print("val_docs:", len(val))

if __name__ == "__main__":
    main()
