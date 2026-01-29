#!/bin/bash
#SBATCH -J portcheck_w1_to_w2
#SBATCH -p debug
#SBATCH -N 1
#SBATCH -w worker1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH --time=00:02:00
#SBATCH -o logs/%x-%j.out
#SBATCH -e logs/%x-%j.err

echo "host=$(hostname) date=$(date)"
python3 - <<'PY'
import socket
target=("192.168.34.18", 6818)  # worker2 slurmd port
s=socket.socket()
s.settimeout(2)
try:
    s.connect(target)
    print(f"OK connect {target[0]}:{target[1]}")
except Exception as e:
    print(f"FAIL connect {target[0]}:{target[1]} -> {e}")
finally:
    s.close()
PY

