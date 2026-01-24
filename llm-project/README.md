# llm-project (GPU/CUDA)

Proyecto reproducible para:

- Preparar dataset local a partir de archivos `.txt`
- Entrenar tokenizer BPE byte-level
- Pretraining desde cero (GPT-2 pequeño configurable)
- Fine-tuning con LoRA (PEFT)
- Inferencia de prueba

> Se asume que el entorno fue creado por Ansible:
> - Micromamba: `/opt/micromamba/bin/micromamba`
> - Env: `llm`

## Provisioning and smoke validation (Ansible)

1) CUDA driver provisioning (pins 580-dkms for Pascal):
```bash
ansible-playbook -i inventario.ini site.yml --tags cuda --diff
```

2) LLM env provisioning (CUDA-enabled PyTorch):
```bash
ansible-playbook -i inventario.ini site.yml --tags llm --diff
```

3) Cluster validation + GPU smoke test:
```bash
ansible-playbook -i inventario.ini site.yml --tags validate --diff
```

Expected outputs:
- `nvidia-smi` shows driver 580.126.09 and Quadro P1000.
- Torch reports `cuda_available True`, `torch.version.cuda 12.4`, and the smoke script prints `cuda_mem_delta` and a numeric `result_sum`.

Troubleshooting:
- If `cuda_available False`, ensure the driver stream is `nvidia-driver:580-dkms`, and re-run `--tags cuda` + `--tags llm`.
- If the smoke script is missing, verify the project path contains `scripts/00_smoke_gpu.py`.

## Flujo mínimo

1) Colocar textos en `data/raw/*.txt`

2) Preparar dataset:
```bash
/opt/micromamba/bin/micromamba run -n llm python scripts/01_prepare_dataset.py --raw_dir data/raw --out_dir data/processed
```

3) Entrenar tokenizer:
```bash
/opt/micromamba/bin/micromamba run -n llm python scripts/02_train_tokenizer.py --input_dir data/processed --out_dir artifacts/tokenizer --vocab_size 32000
```

4) Pretraining:
```bash
/opt/micromamba/bin/micromamba run -n llm python scripts/03_pretrain_from_scratch.py --config configs/pretrain_tiny.yml
```

5) Fine-tuning LoRA:
```bash
/opt/micromamba/bin/micromamba run -n llm python scripts/04_finetune_lora.py --config configs/finetune_lora.yml
```

6) Inferencia:
```bash
/opt/micromamba/bin/micromamba run -n llm python scripts/05_infer.py --model_dir artifacts/checkpoints/pretrain_tiny/final --prompt "Hola, explica CUDA:"
```
