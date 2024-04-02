import torch
from xformers.ops import index_select_cat as _index_select_cat

torch.manual_seed(22)
torch.cuda.manual_seed(22)
torch.cuda.manual_seed_all(22)

def tensor_diff(t1, t2, abs_thresh=0, relative_thresh=0, total_thresh=0.001):
    t1 = t1.detach().float()
    t2 = t2.detach().float()
    if torch.numel(t1) != torch.numel(t2):
        return False
    abs_diff = torch.abs(t1 - t2)
    all_err = abs_diff > (abs_thresh + relative_thresh * torch.abs(t2))
    print("======= all_err sum  = ", all_err.sum(), "============ all_tensor num = ", torch.numel(t2))
    print("======= all_err rate = ", all_err.sum() / torch.numel(t2))


sour1 = torch.randn(8, 394752, dtype=torch.float16).cuda()
sour2 = torch.randn(32, 76800, dtype=torch.float16).cuda()
sour_list = [sour1, sour2]

indi1 = torch.tensor([5,2,3,0], dtype=torch.int64).cuda()
indi2 = torch.tensor([2, 11,  4, 20, 30,  9,  8, 24, 21, 29, 19, 16, 26,  1, 13,  0, 18,  6, 28], dtype=torch.int64).cuda()
indi_list = [indi1, indi2]

# print(_index_select_cat(sour_list, indi_list))
xf_res= _index_select_cat(sour_list, indi_list)
to_res = torch.cat([s[i.long()].flatten() for s, i in zip(sour_list, indi_list)], dim=0)
# print(to_res)

# tensor_diff(xf_res, to_res)



from xformers.ops import scaled_index_add as _scaled_index_add
inputt = torch.randn(8, 257, 1536, dtype=torch.float16).cuda()
index = torch.tensor([4,1,6,7], dtype=torch.int64).cuda()
source = torch.randn(4, 257, 1536, dtype=torch.float16).cuda()
scaling = torch.randn(1536, dtype=torch.float16).cuda()
alpha = 2.0
# print(_scaled_index_add(inputt, index, source, scaling, alpha))
# print(torch.index_add(inputt, dim=0, source=scaling * source, index=index, alpha=alpha))
tor_add_res = torch.index_add(inputt, dim=0, source=scaling * source, index=index, alpha=alpha)
# xfo_add_res = _scaled_index_add(inputt, index, source, scaling, alpha)
# print("tor_add_res = ", tor_add_res.shape, tor_add_res.dtype)
# tensor_diff(tor_add_res, xfo_add_res)




