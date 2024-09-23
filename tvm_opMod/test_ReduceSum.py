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
DEBUG=True
test_dtypes = ["float32", "float16", "int8"]

def create_model(batch_size, shape, axes, keepdims):
    shape = [3, 2, 2]
    axes = np.array([1], dtype=np.int64)
    keepdims = 1
    
    input_x = helper.make_tensor_value_info("input", TensorProto.FLOAT, [shape[0], shape[1], shape[2]])
    output_x = helper.make_tensor_value_info("output", TensorProto.FLOAT, [1, 1, 1])

    node_def = helper.make_node(
        'ReduceSum', # node name
        inputs=['input'], # inputs
        outputs=['output'], # outputs
        keepdims=keepdims, # attributes
        )

    graph_def = helper.make_graph(
        [node_def], # nodes: list of NodeProto
        'reducesum_model', # name (string): graph name
        [input_x], # inputs: list of ValueInfoProto
        [output_x], # outputs: list of ValueInfoProto
        )

    onnx_model = helper.make_model(graph_def, producer_name='onnx-example')
    onnx.checker.check_model(onnx_model)
    print('Model : \n\n{}'.format(onnx.helper.printable_graph(onnx_model.graph)))
    return onnx_model

def run_module_build(onnx_model, target, shape_list, data_type="float32"):
    mod, params = relay.frontend.from_onnx(onnx_model, shape_list, freeze_params=True)
    with tvm.transform.PassContext(opt_level=3):
        if data_type == "float16":
            mod = InferType()(mod)
            mod = ToMixedPrecision(mixed_precision_type="float16")(mod)
        if data_type == "int8":
            with relay.quantize.qconfig(calibrate_mode="global_scale", global_scale=8.0, skip_conv_layers=[]):
                mod = relay.quantize.quantize(mod, params)
        lib = relay.build(mod, target=target, params=params, verbose=DEBUG)
    return lib

def check_result(a, b, atol, rtol):
    diff = np.abs(a - b)
    comp = atol + rtol * np.abs(b)
    lag = diff - comp # If lag > 0, this is a failed case
    num_failed = np.sum(lag > 0)
    has_passed = num_failed == 0
    return has_passed

def verify_ReduceSum(batch_size, shape, axes, keepdims, dtype="float32"):

    in_dtype = "float32"
    in_shape = (shape[0], shape[1], shape[2])

    onnx_model = create_model(batch_size, shape, axes, keepdims)

    print("verify_reducesum_tcu, dtype:", dtype, ", batch_size", batch_size,
          ", shape:", shape, ", axes:", axes, ", keepdims:", keepdims)

    def gen_data():
        np.random.seed(12345)
        if dtype == "int8":
            x_np = np.random.randint(-128, 127, in_shape).astype(in_dtype)
        else:
            x_np = np.random.uniform(-1, 1, in_shape).astype(in_dtype)

        return x_np

    x_np  = gen_data()
    x_data = tvm.nd.array(x_np)

    shape_list = {"input": [shape[0], shape[1], shape[2]]}

    def run(device):
        dev = tvm.device(device, 0)
        target = tvm.target.Target(device)
        print("Running on target: %s" % device)
        with autotvm.tophub.context(target):
            lib = run_module_build(onnx_model, target, shape_list, dtype)
            if DEBUG:
                print(lib.function_metadata["__tvm_main__"])
            graph_module = tvm.contrib.graph_executor.GraphModule(lib["default"](dev))
            graph_module.set_input("input", x_data)
            graph_module.run()
            out = graph_module.get_output(0).numpy()

            if "llvm" in device:
                return out
            # evaluate
            ftimer = graph_module.module.time_evaluator("run", dev, number=10, repeat=1)
            prof_res = np.array(ftimer().results) * 1000  # convert to millisecond
            print(
                "\nDevice %s Mean time (std dev): %.2f ms (%.2f ms)\n"
                % (device, np.mean(prof_res), np.std(prof_res))
            )

            return out

    devices = ["iluvatar", "llvm"]
    y_llvm = run(devices[1])
    y_iluvatar = run(devices[0])
    global failures
    global index
    index += 1
    passed = check_result(y_llvm, y_iluvatar, rtol=1e-04, atol=1e-04)
    if passed:
        print(f"!!!---Test {index//len(test_dtypes)} type:{dtype} pass---") # division symbol // gives integer result
    else:
        failures += 1
        print(f"!!!---Test {index//len(test_dtypes)} type:{dtype} failed---, total failures number {failures} :")

if __name__ == "__main__":
    batch_size = 1 
    shape = [3, 2, 2]
    axes = np.array([], dtype=np.int64) 
    keepdims = 1
    for dtype in test_dtypes:
        verify_ReduceSum(batch_size, shape, axes, keepdims, dtype=dtype)
