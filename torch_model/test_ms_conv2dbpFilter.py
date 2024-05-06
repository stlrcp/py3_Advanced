import os
import sys
import time
import numpy as np
import logging as py_logging
import mindspore.context as context
import mindspore.nn as nn
import mindspore.ops.operations._grad_ops as G
from mindspore import Tensor
from mindspore.ops import operations as P
from mindspore import ops
import mindspore
from mindspore.ops import grad

class conv2dfl(nn.Cell):
    def __init__(self):
        super(conv2dfl, self).__init__()
        self.Conv2dFl = G.Conv2DBackpropFilter(128, 3, pad_mode="same", pad=0, pad_list=(1, 1, 1, 1), mode=1, stride=(1, 1), dilation=(1, 1, 1, 1), group=128)
        self.get_shape = P.Shape()


    def construct(self, out, x, w):
        out = self.Conv2dFl(out, x, self.get_shape(w))
        return out

np_dtype = np.float32

np_x = Tensor(np.random.randn(256, 128, 56, 56).astype(np_dtype), mindspore.float32)
np_out = Tensor(np.random.randn(256, 128, 56, 56).astype(np_dtype), mindspore.float32)
np_w = Tensor(np.random.randn(128, 1, 3, 3).astype(np_dtype), mindspore.float32)

context.set_context(mode=context.GRAPH_MODE, device_target="CPU")
net = conv2dfl()
out_cpu = net(np_out, np_x, np_w)

context.set_context(mode=context.GRAPH_MODE, device_target="GPU")
net = conv2dfl()
out_gpu = net(np_out, np_x, np_w)
