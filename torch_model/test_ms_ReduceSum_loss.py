import os
import sys
import time
import numpy as np
import mindspore as ms
import mindspore.context as context
import mindspore.nn as nn
import mindspore.ops.operations._grad_ops as G
from mindspore import Tensor
from mindspore.ops import operations as P

import mindspore.ops.operations as P
from mindspore.nn.loss.loss import LossBase
from mindspore.ops import functional as F

class NLLLoss(LossBase):
    def __init__(self, reduction='mean'):
        super(NLLLoss, self).__init__(reduction)
        self.one_hot = P.OneHot()
        self.reduce_sum = P.ReduceSum()

    def construct(self, logits, label):
        label_one_hot = self.one_hot(label, F.shape(logits)[-1], F.scalar_to_array(1.0), F.scalar_to_array(0.0))
        loss = self.reduce_sum(-1.0 * logits * label_one_hot, (1,))
        return self.get_loss(loss)

np_dtype = np.float32

np_logits = np.random.randn(16, 6113).astype(np_dtype)
np_label = np.random.randn(16,).astype(np.int32)

context.set_context(mode=context.GRAPH_MODE, device_target="CPU")
net = NLLLoss()
np_logits = Tensor(np_logits)
np_label = Tensor(np_label)
values_cpu = net(np_logits, np_label)

context.set_context(mode=context.GRAPH_MODE, device_target="GPU")
net = NLLLoss()
np_logits = Tensor(np_logits)
np_label = Tensor(np_label)
values_gpu = net(np_logits, np_label)
