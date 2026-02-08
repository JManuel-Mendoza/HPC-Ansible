import argparse
import random
from pathlib import Path

import numpy as np
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
    set_seed,
)

from peft import LoraConfig, get_peft_model, TaskType

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

    base_model_dir = cfg["paths"]["base_model_dir"]
    processed_dir = Path(cfg["paths"]["processed_dir"])
    output_dir = ensure_dir(cfg["paths"]["output_dir"])

    train_file = cfg["data"]["train_file"]
    val_file = cfg["data"]["val_file"]
    block_size = int(cfg["data"]["block_size"])

    tok = AutoTokenizer.from_pretrained(base_model_dir, use_fast=True)
    if tok.pad_token is None:
        tok.add_special_tokens({"pad_token": "<pad>"})

    model = AutoModelForCausalLM.from_pretrained(base_model_dir)
    model.resize_token_embeddings(len(tok))

    l = cfg["lora"]
    lora_cfg = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=int(l["r"]),
        lora_alpha=int(l["lora_alpha"]),
        lora_dropout=float(l["lora_dropout"]),
        target_modules=list(l["target_modules"]),
        bias="none",
    )
    model = get_peft_model(model, lora_cfg)

    ds = load_text_dataset(processed_dir, train_file, val_file)

    def tokenize_fn(batch):
        return tok(batch["text"])

    tokenized = ds.map(tokenize_fn, batched=True, remove_columns=["text"])
    lm_ds = tokenized.map(lambda x: group_texts(x, block_size), batched=True)

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
    model.save_pretrained(str(final_dir))
    tok.save_pretrained(str(final_dir))
    print("OK ->", str(final_dir))

if __name__ == "__main__":
    main()
