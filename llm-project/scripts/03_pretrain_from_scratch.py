import argparse
import random
from pathlib import Path

import numpy as np
import torch
from transformers import (
    GPT2Config,
    GPT2LMHeadModel,
    GPT2TokenizerFast,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
    set_seed,
)

from _config import load_yaml, ensure_dir
from _data import load_text_dataset, group_texts

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    cfg = load_yaml(args.config)
    seed = int(cfg.get("seed", 42))
    set_seed(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    processed_dir = Path(cfg["paths"]["processed_dir"])
    tokenizer_dir = Path(cfg["paths"]["tokenizer_dir"])
    output_dir = ensure_dir(cfg["paths"]["output_dir"])

    train_file = cfg["data"]["train_file"]
    val_file = cfg["data"]["val_file"]
    block_size = int(cfg["data"]["block_size"])

    tok = GPT2TokenizerFast.from_pretrained(str(tokenizer_dir))
    if tok.pad_token is None:
        tok.add_special_tokens({"pad_token": "<pad>"})

    ds = load_text_dataset(processed_dir, train_file, val_file)

    def tokenize_fn(batch):
        return tok(batch["text"])

    tokenized = ds.map(tokenize_fn, batched=True, remove_columns=["text"])
    lm_ds = tokenized.map(lambda x: group_texts(x, block_size), batched=True)

    m = cfg["model"]
    model_cfg = GPT2Config(
        vocab_size=len(tok),
        n_positions=int(m["n_positions"]),
        n_ctx=int(m["n_positions"]),
        n_embd=int(m["n_embd"]),
        n_layer=int(m["n_layer"]),
        n_head=int(m["n_head"]),
        bos_token_id=tok.bos_token_id or 0,
        eos_token_id=tok.eos_token_id or 2,
    )
    model = GPT2LMHeadModel(model_cfg)
    model.resize_token_embeddings(len(tok))

    collator = DataCollatorForLanguageModeling(tokenizer=tok, mlm=False)

    t = cfg["train"]
    args_tr = TrainingArguments(
        output_dir=str(output_dir),
        run_name=cfg["run_name"],
        per_device_train_batch_size=int(t["per_device_train_batch_size"]),
        per_device_eval_batch_size=int(t["per_device_eval_batch_size"]),
        gradient_accumulation_steps=int(t["gradient_accumulation_steps"]),
        learning_rate=float(t["learning_rate"]),
        warmup_steps=int(t["warmup_steps"]),
        num_train_epochs=float(t["num_train_epochs"]),
        weight_decay=float(t["weight_decay"]),
        logging_steps=int(t["logging_steps"]),
        evaluation_strategy="steps",
        eval_steps=int(t["eval_steps"]),
        save_strategy="steps",
        save_steps=int(t["save_steps"]),
        save_total_limit=int(t["save_total_limit"]),
        fp16=bool(t.get("fp16", False)),
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=args_tr,
        train_dataset=lm_ds["train"],
        eval_dataset=lm_ds["validation"],
        tokenizer=tok,
        data_collator=collator,
    )

    trainer.train()

    final_dir = Path(output_dir) / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    trainer.save_model(str(final_dir))
    tok.save_pretrained(str(final_dir))
    print("OK ->", str(final_dir))

if __name__ == "__main__":
    main()
