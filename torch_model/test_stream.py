import torch
from torch.distributed.pipeline.sync.stream import (
    new_stream,
    record_stream,
    use_stream,
)
def cuda_sleep(seconds):
    # Warm-up CUDA.
    torch.empty(1, device="cuda")

    # From test/test_cuda.py in PyTorch.
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    start.record()
    torch.cuda._sleep(1000000)
    end.record()
    end.synchronize()
    cycles_per_ms = 1000000 / start.elapsed_time(end)

    torch.cuda._sleep(int(seconds * cycles_per_ms * 1000))

print("======== test start ======")
stream_alloc = new_stream(torch.device("cuda"))
with torch.cuda.stream(stream_alloc):
    x = torch.rand(1, device=torch.device("cuda"))

stream = new_stream(torch.device("cuda"))

record_stream(x, stream)
with use_stream(stream):
    cuda_sleep(0.5)

# 'x' is deleted at Python's perspective. But the block of 'x' is still
# required for 'stream'. 'y' shouldn't be allocated to the block.
data_ptr = x.data_ptr()
del x
stream_alloc.synchronize()
with torch.cuda.stream(stream_alloc):
    y = torch.rand(1, device=torch.device("cuda"))

print("y.data_ptr(): ", y.data_ptr(), ", data_ptr: ", data_ptr)
if y.data_ptr() != data_ptr:
    print("======== test pass ======")
else:
    print("======== test fail ======")
