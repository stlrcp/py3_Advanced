import torch
import torch.nn as nn
import torch.optim as optim

x = torch.tensor([5.0], requires_grad=True) 
y = torch.tensor([10.0], requires_grad=True) 

def tmp_para(input):
    f_value = input * x * x + y*y
    return f_value

def run(t):
    t = torch.tensor([t], requires_grad=True)
    optimizer = optim.SGD([x, y], lr=0.1)
    for i in range(10):
        optimizer.zero_grad()
        f_value = tmp_para(t)
        print("x={:.4f}, y={:.4f}, value={:.4f}".format(x.item(), y.item(), f_value.item()))
        f_value.backward()
        print("x.grad={:.4f}, y.grad={:.4f}".format(x.grad.item(), y.grad.item()))
        optimizer.step()
 
if __name__ == '__main__':
    run(1.0)
