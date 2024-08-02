import torch
import torch.distributed as dist
import torch.multiprocessing as mp
import os
# import torch_dipu

def worker(rank, world_size):
    dist.init_process_group("nccl", rank=rank, world_size=world_size)
    print("after dist init ....")
    tensor = torch.tensor(rank + 1, dtype=torch.float).cuda(rank)
    print(tensor)
    dist.all_reduce(tensor, op=dist.ReduceOp.SUM)
    if rank == 0:
        print(f"Sum of ranks: {tensor.item()}")
    dist.destroy_process_group()

def main(world_size):
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '29500'
    mp.set_start_method('spawn')
    mp.spawn(worker, args=(world_size,), nprocs=world_size, join=True)

if __name__ == "__main__":
    main(4)  # Number of processes
