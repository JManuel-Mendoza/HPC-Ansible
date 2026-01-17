import sys
import torch

def main() -> int:
    print("torch:", torch.__version__)
    print("torch.version.cuda:", torch.version.cuda)
    print("cuda_available:", torch.cuda.is_available())
    if not torch.cuda.is_available():
        print("cuda_device: no-gpu")
        return 1
    device_name = torch.cuda.get_device_name(0)
    before = torch.cuda.memory_allocated()
    a = torch.randn((128, 128), device="cuda")
    b = torch.randn((128, 128), device="cuda")
    c = a @ b
    torch.cuda.synchronize()
    after = torch.cuda.memory_allocated()
    print("cuda_device:", device_name)
    print("cuda_mem_before:", before)
    print("cuda_mem_after:", after)
    print("cuda_mem_delta:", after - before)
    print("result_sum:", float(c.sum().item()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
