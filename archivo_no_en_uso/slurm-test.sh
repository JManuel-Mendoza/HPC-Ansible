#!/bin/sh
#SBATCH -J GPU-Juan
#SBATCH -p gpu
#SBATCH -n 5 
##SBATCH -N 1
#SBATCH -o gpu_%j.out
#SBATCH -e gpu_%j.err
##SBATCH -w worker1

echo "Hola Mundo PUJ soy un Batch"
echo "Hostname is: " $(hostname -f)
echo "Espero por 10 s"
echo "My SLURM_NTASKS: " $SLURM_NTASKS
sleep 5
echo "Corriendo en GPU"

eval "$(micromamba shell hook --shell bash)"
micromamba activate llm
cd /home/sistemas/test-gpu/gpu-demo/demo1_gpu_basics
srun python vector_multiply_gpu.py 1000000
echo "Fin"
