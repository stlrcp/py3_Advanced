import torch
import torch.nn as nn

torch.manual_seed(2)
torch.cuda.manual_seed_all(2)

# torch.backends.cudnn.enabled = False

# 定义一个简单的LSTM模型
class SimpleLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=1, batch_first=True):
        super(SimpleLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers=num_layers, batch_first=batch_first)

    def forward(self, x, hidden=None):
        out, hidden = self.lstm(x, hidden)
        return out, hidden

model0 = SimpleLSTM(input_size=128, hidden_size=128).cuda()
model_dict = model0.state_dict()

x = torch.randn(32, 50, 128).cuda().requires_grad_(True)  # (batch_size, sequence_length, input_size)
d = torch.randn(32, 50, 128).cuda()

# 隐藏状态初始化
h0 = torch.zeros(1, x.size(0), model0.lstm.hidden_size).cuda()
c0 = torch.zeros(1, x.size(0), model0.lstm.hidden_size).cuda()

# 正向传播
out0, _ = model0(x, (h0, c0))

# 反向传播及参数更新
out0.backward(d)

model_para = model0.parameters()
# print(model_para)

weight0_grad0 = next(model_para).grad
weight1_grad0 = next(model_para).grad
bias0_grad0 = next(model_para).grad
bias1_grad0 = next(model_para).grad


torch.backends.cudnn.enabled = False
model1 = SimpleLSTM(input_size=128, hidden_size=128).cuda()
model1.load_state_dict(model_dict)
out1, _ = model1(x, (h0, c0))
out1.backward(d)
model_para1 = model1.parameters()
weight0_grad1 = next(model_para1).grad
weight1_grad1 = next(model_para1).grad
bias0_grad1 = next(model_para1).grad
bias1_grad1 = next(model_para1).grad

def tensor_diff(t1, t2, abs_thresh=1e-5, relative_thresh=1e-5, total_thresh=0.001):
    t1 = t1.detach().float()
    t2 = t2.detach().float()
    if torch.numel(t1) != torch.numel(t2):
        return False
    abs_diff = torch.abs(t1 - t2)
    all_err = abs_diff > (abs_thresh + relative_thresh * torch.abs(t2))
    print("======= all_err sum  = ", all_err.sum(), "============ all_tensor num = ", torch.numel(t2))
    print("======= all_err rate = ", all_err.sum() / torch.numel(t2))

tensor_diff(weight0_grad0, weight0_grad1)
tensor_diff(weight1_grad0, weight1_grad1)
tensor_diff(bias0_grad0, bias0_grad1)
tensor_diff(bias1_grad0, bias1_grad1)

# torch.save(next(model_para).grad, 'weght0_grad.pth')
# torch.save(next(model_para).grad, 'weght1_grad.pth')
# torch.save(next(model_para).grad, 'bias0_grad.pth')
# torch.save(next(model_para).grad, 'bias1_grad.pth')

