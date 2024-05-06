import os
import sys
import time
import numpy as np
import mindspore.context as context
import mindspore.nn as nn
import mindspore.ops.operations._grad_ops as G
from mindspore import Tensor
from mindspore.ops import operations as P
import mindspore


class BiasAddGradNet(nn.Cell):
    def __init__(self):
        super(BiasAddGradNet, self).__init__()
        self.biasaddgrad = G.BiasAddGrad()

    def construct(self, x):
        return self.biasaddgrad(x)


np_dtype = np.float32
input_x = Tensor(np.arange(97808).reshape((16, 6113)), mindspore.float32)

context.set_context(mode=context.GRAPH_MODE, device_target="CPU")
net = BiasAddGradNet()
cpu_out = net(input_x)

context.set_context(mode=context.GRAPH_MODE, device_target="GPU")
net = BiasAddGradNet()
gpu_out = net(input_x)
