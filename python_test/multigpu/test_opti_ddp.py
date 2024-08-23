import os
import torch
from torch.nn import Module
from torch.optim import Adam
import torch.distributed as dist
import torch.multiprocessing as mp
import torch.nn as nn
from torch.nn.parallel import DistributedDataParallel as DDP
torch.manual_seed(20)
os.environ['MASTER_ADDR'] = 'localhost'
os.environ['MASTER_PORT'] = '12345'


class MyModel(Module):
    def __init__(self, in_dim, hidden_dim):
        super(MyModel, self).__init__()
        self.linear = torch.nn.Linear(in_features=in_dim, out_features=hidden_dim, bias=True)
        self.linear2 = torch.nn.Linear(in_features=hidden_dim, out_features=in_dim, bias=False)
    def forward(self, x):
        y = self.linear(x)
        out = self.linear2(y)
        return out
in_dim = 5
hidden_dim = 2
model = MyModel(in_dim=in_dim, hidden_dim=hidden_dim)
# print(model)
# print(model.parameters)
# optimizer = Adam(params=model.parameters(), lr=0.01)
# optimizer = Adam([
#     {'params': model.linear.parameters(), 'lr': 0.05},
#     {'params': model.linear2.parameters()}
# ], lr=0.01)
# print(optimizer)
# print(optimizer.state_dict())
# x = torch.randn((in_dim))
# x = torch.ones_like(x)
x = torch.ones((in_dim))
# print(x)
# out = model(x)
# # print(out)
# l1 = torch.nn.Linear(5, 2)
# # print(l1.weight)
# # print(l1.bias)
# print(l1(x))
# loss = torch.sum(out, dim=-1)
# print(loss)
# print(optimizer.state_dict())
# optimizer.zero_grad()
# loss.backward()
# optimizer.step()
# for i in range(12):
#     out = model(x)
#     loss = torch.sum(out, dim=-1).abs().sum()
#     optimizer.zero_grad()
#     loss.backward()
#     optimizer.step()
    
# print(optimizer.state_dict())

def example(rank, world_size):
    dist.init_process_group("nccl", rank=rank, world_size=world_size)
    
    in_dim = 5
    hidden_dim = 2
    # model = MyModel(in_dim=in_dim, hidden_dim=hidden_dim).to(rank)
    model = torch.nn.Sequential(
        torch.nn.Linear(5, 4),
        torch.nn.Linear(4, 4),
        torch.nn.Linear(4, 2)
    ).to(rank)
    
    print(model)
    x = torch.randn((in_dim)).to(rank)
    ddp_model = DDP(model, device_ids=[rank])
    optimizer = Adam(params=ddp_model.parameters(), lr=0.01)
    for i in range(12):
        output = ddp_model(x)
        loss = torch.sum(output, dim=-1).abs().sum()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(optimizer.state_dict())
    
def main():
    world_size = 2
    mp.spawn(example, args=(world_size,), nprocs=world_size, join=True)
    
if __name__ == "__main__":
    main()
