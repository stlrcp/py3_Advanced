import sys


for i in range(10):
    if i > 3:
        print(i)
        #sys.exit(100)

a = 100
b = 0
c = a / b


'''
import torch
import torch.nn as nn
import numpy as np

import torch.optim as optim

seed = 2222
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.cuda.manual_seed_all(seed)



class ConvModel(nn.Module):
    def __init__(self):
        super(ConvModel, self).__init__()
        
        # 定义卷积层
        self.conv = nn.Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        
    def forward(self, x):
        # 卷积操作
        x = self.conv(x)
        return x

input = torch.randn(1, 128, 100, 152, requires_grad=True).cuda()
model = ConvModel().cuda()
optimizer = optim.SGD(model.parameters(), lr=0.005, momentum=0.9)

output = model(input)

print(input.mean())
for para in model.parameters():
    print("the forward weigt = ", para.mean(), para.size())

output.backward(torch.ones_like(output))

optimizer.step()

print(output.mean())
for para in model.parameters():
    print("the backward weigt = ", para.mean(), para.size())
'''


"""
#### 测试 matmul 的 backward 用法
import torch
from torch.autograd import Variable
import torch.nn as nn

torch.manual_seed(2)
torch.cuda.manual_seed_all(2)

a = torch.randn(256,28, 29, 128).cuda().requires_grad_(True)
b = torch.randn(128).cuda().requires_grad_(True)
c = a.matmul(b)
# print(c.shape)
d = torch.randn(256, 28, 29).cuda()
# torch.save(a, "a_1.pth")
# torch.save(b, "b_1.pth")
# torch.save(d, "d_1.pth")
c.backward(d)
# print(a.grad)
# print(b.grad)
torch.save(a.grad, "a_g_1.pth")
torch.save(b.grad, "b_g_1.pth")
"""
