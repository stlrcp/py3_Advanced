import numpy as np
import time
import os
import onnx
from onnx import helper
from onnx import TensorProto
import pandas as pd

import tvm
from tvm import autotvm
from tvm import relay
from tvm.relay.transform import InferType, ToMixedPrecision

failures=0
index=0
DEBUG=False

test_dtypes = ["float32", "float16", "int8"]

def create_model(batch_size, in_channel, in_size, num_filter, kernel_size, stride, padding, data_type="float32"):
    if data_type == "float32":  # we only create onnx model in fp32 for now
        in_dtype = onnx.TensorProto.FLOAT
        kernel_dtype = onnx.TensorProto.FLOAT
        out_dtype = onnx.TensorProto.FLOAT
    else:
        print("Not supported data type")

    weight = np.random.randn(num_filter * in_channel * kernel_size * kernel_size)
    bias = np.random.randn(num_filter)
    out_size = int(((in_size - kernel_size + 2 * padding)/stride) + 1)
    X = helper.make_tensor_value_info('input', in_dtype, [batch_size, in_channel, in_size, in_size])
    W = helper.make_tensor('W', kernel_dtype, [num_filter, in_channel, kernel_size, kernel_size], weight)
    B = helper.make_tensor('B', kernel_dtype, [num_filter], bias)
    Y = helper.make_tensor_value_info('output', out_dtype, [batch_size, num_filter, out_size, out_size])
    node_def = helper.make_node(
        op_type='Conv', # node name
        inputs=['input', 'W', 'B'],
        outputs=['output'],
        # attributes
        strides=[stride, stride],
        pads=[padding, padding],
        )
    
    graph_def = helper.make_graph(
        nodes=[node_def],
        name='conv_model',
        inputs=[X], # graph inputs
        outputs=[Y], # graph outputs
        initializer=[W, B],
    )
    onnx_model = helper.make_model(graph_def, producer_name='onnx-example')
    onnx.checker.check_model(onnx_model)
    if DEBUG:
        print('Model :\n\n{}'.format(onnx.helper.printable_graph(onnx_model.graph)))
    return onnx_model

def run_module_build(onnx_model, target, shape_list, batch_size, data_type="float32"):
    mod, params = relay.frontend.from_onnx(onnx_model, shape_list, freeze_params=True)
    with tvm.transform.PassContext(opt_level=3):
        layouts = {
            'nn.conv2d': ["NHWC", 'default'],
        }
        seq = tvm.transform.Sequential(
            [
                relay.transform.ConvertLayout(layouts),
                relay.transform.FoldConstant(),
                relay.transform.InferType(),
            ]
        )
        mod = seq(mod)
        if data_type == "float16":   
            mod = InferType()(mod)    
            mod = ToMixedPrecision(mixed_precision_type="float16")(mod)    
        if data_type == "int8":
            with relay.quantize.qconfig(calibrate_mode="global_scale", global_scale=8.0, skip_conv_layers=[]):
                mod = relay.quantize.quantize(mod, params)
        lib = relay.build(mod, target=target, params=params, verbose=DEBUG)
    return lib

def check_result(a, b, atol, rtol, total_thresh=0.001):
    diff = np.abs(a - b)
    t_df = 1
    for i in range(len(diff.shape)):
        t_df = t_df * (diff.shape[i])
    comp = atol + rtol * np.abs(b)
    lag = diff - comp # If lag > 0, this is a failed case
    num_failed = np.sum(lag > 0)
    has_passed = (num_failed / t_df) < total_thresh
    if not has_passed:
        n_print = 10
        idx_n = (-lag).argsort(axis=None)[:n_print]
        print(f"Print max_diff top {n_print} values...")
        for i in range(n_print):
            idx_i = idx_n[i]
            pos_i = np.unravel_index(idx_i, a.shape)
            print(f"{i}: idx = {idx_i}, pos = {pos_i}, cpu = {a[pos_i]:.4f}, gpu = {b[pos_i]:.4f},"
            f" diff = {diff[pos_i]:.4f}, comp = {comp[pos_i]:.4f}, lag = {lag[pos_i]:.4f}")
    return has_passed

def verify_conv2d(batch, in_channel, in_size,
                        num_filter, kernel_size,
                        stride, padding, dilation=1,
                        dtype="float32"):
    data_layout = "NCHW"
    in_shape = (batch, in_channel, in_size, in_size)
    weight_shape = (num_filter, in_channel, kernel_size, kernel_size)
    in_dtype="float32"
    
    # build model in ONNX format
    shape_list = {"input": [batch, in_channel, in_size, in_size]}
    onnx_model = create_model(batch, in_channel, in_size, num_filter, kernel_size, stride, padding)

    print("verify_conv2d_tcu, dtype:", dtype, "data_layout:", data_layout,
          ", in_shape:", in_shape, ", weight_shape:", weight_shape,
          ", strides:", stride, ", padding:", padding, ", dilation:", dilation)

    def gen_data():
        np.random.seed(12345)
        if dtype == "int8":
            x_np = np.random.randint(-128, 127, in_shape).astype(in_dtype)
            w_np = np.random.randint(-128, 127, weight_shape).astype(dtype)
        else:
            x_np = np.random.uniform(-1, 1, in_shape).astype(in_dtype)
            w_np = np.random.uniform(-1, 1, weight_shape).astype(dtype)

        return x_np, w_np

    x_np, _ = gen_data()
    x_data = tvm.nd.array(x_np)

    def run(device):
        dev = tvm.device(device, 0)
        target = tvm.target.Target(device)
        print("Running on target: %s" % device)
        with autotvm.tophub.context(target):
            lib = run_module_build(onnx_model, target, shape_list, batch, dtype)
            if DEBUG:
                print(lib.function_metadata["__tvm_main__"])
            graph_module = tvm.contrib.graph_executor.GraphModule(lib["default"](dev))
            graph_module.set_input("input", x_data)
            graph_module.run()
            out = graph_module.get_output(0).numpy()

            return out

    devices = ["iluvatar", "llvm"]
    y_llvm = run(devices[1])
    y_iluvatar = run(devices[0])
    global failures
    global index
    index += 1 
    if dtype == "float16":
        #passed = check_result(y_llvm, y_iluvatar, rtol=1e-3, atol=1e-3, total_thresh=0.001)
        passed = check_result(y_llvm, y_iluvatar, rtol=1e-3, atol=1e-2, total_thresh=0.001)
    else:
        passed = check_result(y_llvm, y_iluvatar, rtol=1e-04, atol=1e-05, total_thresh=0.001)
    if passed:
        print(f"!!!---Test {index//len(test_dtypes)} type:{dtype} pass---") # division symbol // gives integer result 
    else:
        failures += 1
        print(f"!!!---Test {index//len(test_dtypes)} type:{dtype} failed---, total failures number {failures} :")

if __name__ == "__main__":
    N, C, W, OutC, kw, sh, pw = 8, 3, 108, 64, 3, 1, 1
    for dtype in test_dtypes:
        verify_conv2d(N, C, W, OutC, kw, sh, pw, 1, dtype)
