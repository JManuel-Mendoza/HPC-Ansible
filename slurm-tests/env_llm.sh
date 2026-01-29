#!/bin/bash
# Activa el entorno LLM (micromamba) para jobs batch.
set -e

if command -v micromamba >/dev/null 2>&1; then
  eval "$(micromamba shell hook --shell bash)"

  # Evita fallos por variables no definidas en scripts activate.d (MKL, etc.)
  export MKL_INTERFACE_LAYER="${MKL_INTERFACE_LAYER:-}"

  micromamba activate llm
else
  echo "ERROR: micromamba no está en PATH"
  exit 1
fi
