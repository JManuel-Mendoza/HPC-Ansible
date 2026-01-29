#!/usr/bin/env python3
import os, socket, time
import torch
import torch.distributed as dist

def env_int(k, default=None):
    v = os.environ.get(k, None)
    return default if v is None else int(v)

def main():
    # Slurm-friendly: usa RANK/WORLD_SIZE si existen, si no usa SLURM_*
    rank = int(os.getenv("RANK", os.getenv("SLURM_PROCID", "-1")))
    world = int(os.getenv("WORLD_SIZE", os.getenv("SLURM_NTASKS", "-1")))
    if rank < 0 or world < 1:
        raise RuntimeError("No pude inferir rank/world. Revisa SLURM_PROCID y SLURM_NTASKS.")

    master_addr = os.environ.get("MASTER_ADDR", None)
    master_port = os.environ.get("MASTER_PORT", None)
    if not master_addr or not master_port:
        raise RuntimeError("Faltan MASTER_ADDR/MASTER_PORT")

    backend = os.environ.get("TORCH_DIST_BACKEND", "gloo")

    dist.init_process_group(backend=backend, init_method="env://", rank=rank, world_size=world)

    host = socket.gethostname()
    print(f"[rank {rank}/{world}] host={host} backend={backend}")

    # Sanity: allreduce suma de ranks
    x = torch.tensor([float(rank)], dtype=torch.float32)
    dist.all_reduce(x, op=dist.ReduceOp.SUM)
    expected = (world - 1) * world / 2.0
    ok = abs(x.item() - expected) < 1e-4
    if rank == 0:
        print(f"allreduce_sum={x.item():.0f} expected={expected:.0f} {'OK' if ok else 'FAIL'}")

    # Micro-bench: allreduce sobre tensores de distinto tamaño
    # (esto aproxima el costo de sincronizar gradientes)
    sizes_bytes = [1024, 64*1024, 1024*1024, 4*1024*1024]  # 1KiB..4MiB
    iters = 200
    warmup = 20

    for b in sizes_bytes:
        n = max(1, b // 4)  # float32
        t = torch.ones(n, dtype=torch.float32)

        for _ in range(warmup):
            dist.all_reduce(t, op=dist.ReduceOp.SUM)

        dist.barrier()
        t0 = time.time()
        for _ in range(iters):
            dist.all_reduce(t, op=dist.ReduceOp.SUM)
        dist.barrier()
        t1 = time.time()

        avg = (t1 - t0) / iters

        # Regla práctica: allreduce mueve ~O(bytes) por iteración; aquí reporto “effective” simple
        eff_MBps = (b / avg) / 1e6
        if rank == 0:
            print(f"allreduce size={b} bytes avg={avg*1e3:.3f} ms  approx_effective={eff_MBps:.1f} MB/s")

    dist.destroy_process_group()

if __name__ == "__main__":
    main()
