import os
import argparse
import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForLanguageModeling,
    TrainingArguments,
    Trainer,
    set_seed,
)

def add_the_end(example):
    txt = (example.get("text") or "").strip()
    if not txt:
        example["text"] = "The end."
        return example
    if not txt.endswith((".", "!", "?", "\"", "'")):
        txt = txt + "."
    example["text"] = txt + "\nThe end."
    return example

def group_texts(examples, block_size: int):
    concatenated = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = len(concatenated["input_ids"])
    if total_length >= block_size:
        total_length = (total_length // block_size) * block_size
    result = {
        k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
        for k, t in concatenated.items()
    }
    result["labels"] = result["input_ids"].copy()
    return result

def make_training_args(**kwargs):
    """
    Compat layer: transformers 4.x usa evaluation_strategy,
    transformers 5.x usa eval_strategy.
    """
    try:
        return TrainingArguments(**kwargs)
    except TypeError as e:
        msg = str(e)
        if "evaluation_strategy" in msg:
            # transformers v5 expects eval_strategy
            v = kwargs.pop("evaluation_strategy")
            kwargs["eval_strategy"] = v
            return TrainingArguments(**kwargs)
        if "eval_strategy" in msg:
            # transformers v4 expects evaluation_strategy
            v = kwargs.pop("eval_strategy")
            kwargs["evaluation_strategy"] = v
            return TrainingArguments(**kwargs)
        raise

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model_name_or_path", required=True)
    p.add_argument("--output_dir", required=True)
    p.add_argument("--cache_dir", default=None)

    p.add_argument("--block_size", type=int, default=256)
    p.add_argument("--max_steps", type=int, default=4000)
    p.add_argument("--learning_rate", type=float, default=5e-5)
    p.add_argument("--warmup_steps", type=int, default=50)
    p.add_argument("--weight_decay", type=float, default=0.0)

    p.add_argument("--per_device_train_batch_size", type=int, default=1)
    p.add_argument("--gradient_accumulation_steps", type=int, default=8)

    p.add_argument("--logging_steps", type=int, default=25)
    p.add_argument("--save_steps", type=int, default=200)
    p.add_argument("--save_total_limit", type=int, default=2)

    p.add_argument("--preproc_workers", type=int, default=4)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    set_seed(args.seed)

    print("=== ENV / CUDA CHECK ===")
    print("Transformers:", __import__("transformers").__version__)
    print("Torch:", torch.__version__)
    print("CUDA available:", torch.cuda.is_available())
    print("CUDA_VISIBLE_DEVICES:", os.environ.get("CUDA_VISIBLE_DEVICES"))
    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))
    print("========================")

    print("Loading dataset TinyStories...")
    ds = load_dataset("roneneldan/TinyStories", cache_dir=args.cache_dir)

    print("Appending 'The end.' to each example...")
    ds = ds.map(add_the_end, num_proc=max(1, args.preproc_workers))

    print("Loading tokenizer/model...")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(args.model_name_or_path)

    def tok_fn(batch):
        return tokenizer(batch["text"])

    print("Tokenizing...")
    tokenized = ds.map(
        tok_fn,
        batched=True,
        num_proc=max(1, args.preproc_workers),
        remove_columns=ds["train"].column_names,
        desc="Tokenizing",
    )

    print(f"Grouping into blocks of {args.block_size}...")
    lm_ds = tokenized.map(
        lambda x: group_texts(x, args.block_size),
        batched=True,
        num_proc=max(1, args.preproc_workers),
        desc=f"Grouping to blocks of {args.block_size}",
    )

    train_ds = lm_ds["train"]
    collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    # Nota: NO usamos overwrite_output_dir (no existe en tu build)
    training_args = make_training_args(
        output_dir=args.output_dir,
        max_steps=args.max_steps,
        per_device_train_batch_size=args.per_device_train_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        warmup_steps=args.warmup_steps,
        weight_decay=args.weight_decay,
        logging_steps=args.logging_steps,
        save_steps=args.save_steps,
        save_total_limit=args.save_total_limit,
        evaluation_strategy="no",  # compat: se convertirá a eval_strategy en v5
        report_to=[],
        seed=args.seed,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        data_collator=collator,
        tokenizer=tokenizer,
    )

    print("=== TRAINING START ===")
    trainer.train()

    print("Saving final model/tokenizer...")
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    print("DONE")

if __name__ == "__main__":
    main()
