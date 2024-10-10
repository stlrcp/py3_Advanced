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


'''
import torch
import torch.nn as nn
import sys

torch.manual_seed(2)
torch.cuda.manual_seed_all(2)

class dropmodel(nn.Module):
    def __init__(self):
        super(dropmodel, self).__init__()
        self.dropout = nn.Dropout(p=0.2)
    def forward(self, inputs):
        out = self.dropout(inputs)
        return out
model = dropmodel().cuda()
inp = torch.randn(255,255,128,3).cuda()
out = model(inp)
print(out)
'''

# https://blog.csdn.net/m0_37602827/article/details/103052518    python 中两个不同 shape 数组间运算规则
import numpy as np
# a = np.array([1,1,1])
# b = np.array([[1,1,1], [2, 2,2]])
# c  = a+1
# d = b+1
# print("c=a+1  ", c)
# print("d=b+1  ", d)
# a = np.array([[1,2,3]])
# b = np.array([[[1], [2], [3], [4], [5], [6]]])
# print(a.shape)
# print(b.shape)
# c = a+b
# d = b+a
# c_mul = a*b
# print("c = ", c, c.shape)
# print("d = ", d, d.shape)
# print("c_mul = ", c_mul, c_mul.shape)
a = np.array([[[1, 1, 1]], [[2, 2, 2]], [[3, 3, 3]]])
b = np.array([[[1],[2], [3]], [[4],[5],[6]], [[7],[8],[9]]])
print(a, a.shape)
print(b, b.shape)
print(a*b)
