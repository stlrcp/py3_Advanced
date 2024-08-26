

import os
import torch
from torch.nn import Module
from torch.optim import Adam
import torch.distributed as dist
import torch.multiprocessing as mp
import torch.nn as nn
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed.optim import ZeroRedundancyOptimizer
torch.manual_seed(20)
os.environ['MASTER_ADDR'] = 'localhost'
os.environ['MASTER_PORT'] = '12345'

def example(rank, world_size):
    dist.init_process_group("nccl", rank=rank, world_size=world_size)
    s_worldsize = dist.get_world_size(dist.group.WORLD)
    s_rank = dist.get_rank(dist.group.WORLD)
    print("s_rank = ", s_rank)
    print("s_worksize = ", s_worldsize)
    for rank_i in range(s_worldsize):
        if s_rank == 0:
            if rank_i == s_rank:
                print("this is in second if, rank_i == s_rank")
            else:
                print("this is the else part")
        else:
            if rank_i == s_rank:
                print("in the first else and this is a if, rank_i == s_rank")
            elif rank_i != 0:
                print("This is a else in the first else, the else part")
                
    
    in_dim = 5
    hidden_dim = 2
    # model = MyModel(in_dim=in_dim, hidden_dim=hidden_dim).to(rank)
    model = torch.nn.Sequential(
        torch.nn.Linear(5, 4),
        torch.nn.Linear(4, 4),
        torch.nn.Linear(4, 2)
    ).to(rank)
    
    # print(model)
    x = torch.randn((in_dim)).to(rank)
    ddp_model = DDP(model, device_ids=[rank])
    optimizer = Adam(params=ddp_model.parameters(), lr=0.01)
    
    sharded_optimizer = ZeroRedundancyOptimizer(
                params=ddp_model.parameters(),
                optimizer_class=torch.optim.Adam,
                lr=0.01)
    
    for i in range(12):
        output = ddp_model(x)
        loss = torch.sum(output, dim=-1).abs().sum()
        # optimizer.zero_grad()
        sharded_optimizer.zero_grad()
        loss.backward()
        # optimizer.step()
        sharded_optimizer.step()
    # print(optimizer.state_dict())
    
    
def main():
    world_size = 4
    mp.spawn(example, args=(world_size,), nprocs=world_size, join=True)
    
if __name__ == "__main__":
    main()
