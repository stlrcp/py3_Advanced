import os
import torch
from torch.nn import Module
from torch.optim import Adam

torch.manual_seed(20)


class MyModel(Module):
    def __init__(self, in_dim, hidden_dim, out_dim):
        super(MyModel, self).__init__()
        self.linear = torch.nn.Linear(in_features=in_dim, out_features=hidden_dim, bias=True)
        self.linear2 = torch.nn.Linear(in_features=hidden_dim, out_features=hidden_dim, bias=True)
        self.linear3 = torch.nn.Linear(in_features=hidden_dim, out_features=out_dim, bias=True)
    def forward(self, x):
        y = self.linear(x)
        out1 = self.linear2(y)
        out2 = self.linear3(out1)
        return out2


model = torch.nn.Sequential(
        torch.nn.Linear(5, 4),
        torch.nn.Linear(4, 4),
        torch.nn.Linear(4, 2)
)

in_dim, hidden_dim, out_dim = 5, 4, 2
model = MyModel(in_dim, hidden_dim, out_dim)

print(model)
print(model.state_dict())
optimizer = Adam(params=model.parameters(), lr=0.01)
print(optimizer.state_dict())
x = torch.randn((in_dim))
output = model(x)
loss = torch.sum(output, dim=-1).abs().sum()
optimizer.zero_grad()
loss.backward()
optimizer.step()
print(optimizer.state_dict())
