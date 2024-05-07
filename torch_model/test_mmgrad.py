import torch
from torch.autograd import Variable

torch.manual_seed(2)
torch.cuda.manual_seed_all(2)

a = torch.randn(256,28, 29, 128).cuda().requires_grad_(True)
b = torch.randn(128).cuda().requires_grad_(True)
c = a.matmul(b)
d = torch.randn(256, 28, 29).cuda()

c.backward(d)
# print(b.grad)
# torch.save(a.grad, "a_g_1.pth")
torch.save(b.grad, "b_g_1.pth")
