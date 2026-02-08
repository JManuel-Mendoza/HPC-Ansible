from __future__ import annotations
from pathlib import Path
from datasets import load_dataset

def load_text_dataset(processed_dir: str | Path, train_file: str, val_file: str):
    processed_dir = str(processed_dir)
    data_files = {
        "train": str(Path(processed_dir) / train_file),
        "validation": str(Path(processed_dir) / val_file),
    }
    return load_dataset("text", data_files=data_files)

def group_texts(examples, block_size: int):
    concatenated = {k: sum(examples[k], []) for k in examples.keys()}
    total_len = len(concatenated["input_ids"])
    total_len = (total_len // block_size) * block_size
    result = {}
    for k, t in concatenated.items():
        result[k] = [t[i:i+block_size] for i in range(0, total_len, block_size)]
    result["labels"] = result["input_ids"].copy()
    return result
