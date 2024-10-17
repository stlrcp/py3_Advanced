#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
from collections import OrderedDict
from functools import partial
import pandas as pd
import os
import random
import argparse
import matplotlib.pyplot as plt
import weakref


eps = 1e-4

archs = ["nv", "bi"]

#cmp_archs[0] is credible
cmp_archs = ["nv", "bi"]


def set_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    #torch.backends.cudnn.deterministic = True
set_seed(40)

def set_fullbackward():
    build_env["full"] = True

def inference_hook(module, F):
    return module.register_forward_hook(F)

def backward_hook(module, F):
    if "full" in build_env:
        return module.register_full_backward_hook(F)
    else:
        return module.register_backward_hook(F)

#binary ops
def max_diff_op(lhs, rhs):
    ans = []
    if (len(lhs) == len(rhs)):
        for i in range(len(lhs)):
            diff = np.abs(lhs[i] - rhs[i])
            ans.append(("%.5f"%np.max(diff).item()))
    else:
        print("Error: sizeof output in not equal", type(lhs))
        exit(1)
    return ans
def max_diff_rate_op(lhs, rhs):
    ans = []
    if (len(lhs) == len(rhs)):
        for i in range(len(lhs)):
            diff = np.abs(lhs[i] - rhs[i])
            ans.append(("%.5f"%np.max(diff / (np.abs(lhs[i]) + eps)).item()))
    else:
        print("Error: sizeof output in not equal", type(lhs))
        exit(1)
    return ans

cmp_Ops={
    "max_diff":max_diff_op,
    "max_diff_rate":max_diff_rate_op,
}

#unitary ops
def mean_op(input):
    if isinstance(input, (list, tuple)):
        return ["%.5f"%np.mean(o).item() for o in input]

def variance_op(input):
    if isinstance(input, (list, tuple)):
        return ["%.5f"%np.var(o).item() for o in input]

def accumulated_op(input):
    if isinstance(input, (list, tuple)):
        return ["%.5f"%np.sum(np.abs(o)).item() for o in input]

def output_shape_op(input):
    if isinstance(input, list):
        return [list(o.shape)[1:] for o in input]
def item_op(input):
    if isinstance(input, list):
        return [o.item() for o in input]

Ops={
    "mean":mean_op,
    "variance":variance_op,
    "accumulate":accumulated_op,
}

Ops_loss={
    "Loss":item_op,
}


# mode record
def add_tensors(input):
    return input.detach().cpu().numpy()

def forward_record(dis:dict, module, input, output):
    dis["record"]["output"] = list(tensor_handler(output, add_tensors))

def backward_record(dis:dict, module, input, output):
    dis["record"]["output_grads"] = list(tensor_handler(output, add_tensors))
    dis["record"]["input_grads"] = list(tensor_handler(input, add_tensors))
    
#select tensors from output
#you should add code elif for your own class,or provide hasattr(raw_data)
#raw_data should return a container(sometimes output is not unique)
def own_class_handler(input, Op):
    if hasattr(input, "raw_data"):
        for val in input.raw_data():
            return Op(val)
    else:
        print("this model use class: %s,please check whether if these classes hasattr(raw_data)"%type(input))

#select tensor from classes 
#rnn always use packed data
def PackSequence_handler(input):
    return input.data

def generator_handler(input):
    return list(input)

handler_ops={
    "PackSequence":PackSequence_handler,
    "generator":generator_handler,
}

def dfs_handler(Op, input):
    if isinstance(input, torch.Tensor):
        Op(input)
    elif isinstance(input, (tuple, list)):
        for val in input:
            dfs_handler(Op, val)
    elif isinstance(input, dict):
        for key in input:
            dfs_handler(Op, input[key])
    else:
        own_class_handler(input, Op)

def tensor_handler(input, Op):
    queue = []
    queue.append(input)
    while len(queue) > 0:
        front = queue[0]
        if isinstance(front, torch.Tensor):
            yield Op(front)
        elif isinstance(front, (tuple, list)):
            for val in front:
                queue.append(val)
        elif isinstance(front, dict):
            for key in front:
                queue.append(front[key])

        elif str(type(front))  in handler_ops:
            queue.append(handler_ops[str(type(front))](front))

        else:
            print("other type :", type(front))
            own_class_handler(front, Op)
        queue.pop(0)

#in future config maybe a class  
#class inference_base:
#    def __init__(self):
#
#        
#
#class loss_hook(inference_base):
#
#class inference_hook(inference_base):

#output_names
forward_output_config=["layer_out"]
backward_output_config=["layer_out", "grad_input", "grad_output"]

class hook_function:
    def __init__(self, f, record_f, name):
        self.fun = f
        self.record_fun = record_f
        self.name = name
    def get_fun(self):
        return self.fun
    def get_record_fun(self):
        return self.record_fun

inference_hook_function = hook_function(inference_hook, forward_record, "inference")
backward_hook_function = hook_function(backward_hook, backward_record, "backward")

hook_config={
    "inference":{
        "Ops":Ops,
        "cmp_Ops":cmp_Ops,
        "option":{
            "call":True,
            "input_shape":True,
            "output_shape":True,
            "weight_shape":False,
        },
        "hook_f":[inference_hook_function],
        "output_names":forward_output_config,
    },
    "backward":{
        "Ops":Ops,
        "cmp_Ops":cmp_Ops,
        "option":{
            "call":True,
            "input_shape":True,
            "output_shape":True,
            "weight_shape":True,
        },
        "hook_f":[backward_hook_function, inference_hook_function],
        "output_names":backward_output_config,
    },
    "loss":{
        "Ops":Ops_loss,
        "cmp_Ops":cmp_Ops,
        "option":{
            "call":False,
            "input_shape":False,
            "output_shape":False,
            "weight_shape":False,
            },
        "hook_f":[inference_hook_function],
        "output_names":forward_output_config,
        "graph":True,
    },
}



class hook_debug:
    def __init__(self, 
                 model, 
                 arch="nv",
                 hook_type = "inference",
                 ignore_layers=None,
                 persist_layers = None,
                 if_compare=False,
                 name="debug",
                 skip=2,
                 ):
        #self.log contains name,idx,input_size,output_size,output's mean and variance...
        self.name = name
        self.model = model
        self.skip = skip
        self.depth = 0
        self.module_size = 0
        self.log = OrderedDict()
        self.call_nums = OrderedDict()
        self.call_nums[arch] = -1
        self.back_call_nums = 0
        self.is_last_module = False
        self.is_first_module = False
        self.back_switch = True
        self.hooks = []
        self._hook_type = hook_type
        self.if_compare = if_compare
        self.arch = arch
        self.arch_objs = OrderedDict()
        self.ignore_layers = ignore_layers
        self.persist_layers = persist_layers
        self.bind_hooks(self.hook)
    #hook every layer in model.copy outputs to cpu mem,and store by np.ndarray type
    #notice: double hook is invaild
    def get_forward_index(self):
        self.call_nums[self.arch] += 1
        return self.call_nums[self.arch]
    def get_backward_index(self):
        self.back_call_nums -= 1
        if self.is_last_module and self.back_switch:
            self.back_switch = False
            self.back_call_nums = self.call_nums[self.arch]
        return self.back_call_nums

    def get_module_name(self, module:nn.Module, name):
        arch = self.arch
        class_name = str(module.__class__).split(".")[-1].split("'")[0]
        if name == "backward":
            module_idx = self.get_backward_index()
        else:
            module_idx = self.get_forward_index()
        return "%s-%i" % (class_name, module_idx)
    def fake_hook(self, module, input, output, hook_fun):
        pass
    def skip_by_step(func):
        def wrapper(self, *args, **kwargs):
            if kwargs["hook_fun"].name == "inference":
                self.depth += 1
                if self.depth % self.module_size == 0:
                    self.is_last_module = True
                    self.is_first_module = False
                    self.back_switch = True
                if self.depth % self.module_size == 1:
                    self.is_first_module = True
                    self.is_last_module = False
            if int((self.depth / self.module_size)) % self.skip == 0:
                return func(self, *args, **kwargs)
            else:
                return self.fake_hook(*args, **kwargs)
        return wrapper

    @skip_by_step
    def hook(self, module, input, output, hook_fun):
        arch = self.arch
        m_key = self.get_module_name(module, hook_fun.name)
        if hook_fun.name == "inference" and m_key not in self.log:
            self.log[m_key] = OrderedDict()
            self.log[m_key]["record"] = OrderedDict()
        if m_key in self.log:
            hook_fun.get_record_fun()(self.log[m_key], module, input, output)
        else:
            return

        #cmp_archs[0] is credible
        if arch == cmp_archs[0] and "option" in hook_config[self._hook_type]:
            option = hook_config[self._hook_type]["option"]
            if "call" in option and option["call"]:
                self.log[m_key]["call"] = str(module)
            def get_tensor_size(input):
                return input.size()
            if "input_shape" in option and option["input_shape"]:
                self.log[m_key]["input_shape"] = list(tensor_handler(input, get_tensor_size))
            #output_shape remove batch_size
            if "output_shape" in option and option["output_shape"]:
                self.log[m_key]["output_shape"] = list(tensor_handler(output, get_tensor_size))
            params = 0
            training_params = 0
            self.log[m_key]["nb_params"] = 0
            self.log[m_key]["nb_training_params"] = 0
            parameters = list(module.parameters())  
            if hasattr(module, "parameters") and len(parameters) > 0:
                def get_training_tensor_size(input):
                    if input.requires_grad:
                        return input.size()
                p_shape = list(tensor_handler(parameters, get_tensor_size))
                if option["weight_shape"]:
                    self.log[m_key]["weight_shape"] = p_shape 
                for w in  p_shape:  
                    params += w.numel()
                self.log[m_key]["nb_params"] = params
                p_train_shape = list(tensor_handler(parameters, get_training_tensor_size))
                for w in  p_train_shape:  
                    training_params += w.numel()
                self.log[m_key]["nb_training_params"] = params
            else:
                if option["weight_shape"]:
                    self.log[m_key]["weight_shape"] = "None"
    #hook entry
    def bind_hooks(self, f):
        module_nums = 0
        for name,child in self.model.named_modules():
            if(len(child._modules.items()) == 0):
                if isinstance(self.persist_layers, set) and name not in self.persist_layers:
                    continue
                if isinstance(self.ignore_layers, set) and name in self.ignore_layers:
                    continue
                module_nums += 1
                self.bind_hook(child, f)
        self.module_size = module_nums
    def bind_hook(self, model, f):
        for hook_function in hook_config[self._hook_type]["hook_f"]:
            self.hooks.append(hook_function.get_fun()(model, partial(f, hook_fun=hook_function)))

        
    #compare("debug.csv", archs)
    def __compare(self, filename, input, layers, cmp_archs, hook_config):
        target = cmp_archs[0]
        cmp_Ops = hook_config["cmp_Ops"]
        Ops = hook_config["Ops"]
        head = ["Layers"]
        option = hook_config["option"]
        for op in option:
            if option[op]:
                head.append(op)
        for name in hook_config["output_names"]:
            for op in Ops:
                for arch in archs:
                    head.append(name + " " + op + "(" + arch + ")")
            for op in cmp_Ops:
                head.append(name + " " + op)
        head.append("Param")
        body = []
        total_params = 0
        total_output = 0
        trainable_params = 0
        for layer in layers:
            arch = cmp_archs[1]
            hook_type = self._hook_type
            tmp_body = []
            tmp_body.append(layer)
            for arg in hook_config["option"]:
                if hook_config["option"][arg]:
                    tmp_body.append(input[target][layer][arg])
            #if "output" not in input[arch][layer]:
            #    tmp_body += ["None" for o in range(0, len(head) - len(tmp_body))]
            #    body.append(tmp_body)
            #    continue
            for key in input[target][layer]["record"]:
                lhs = input[target][layer]["record"][key]
                rhs = input[arch][layer]["record"][key]
                #mean, variance...
                for op in Ops:
                    for arch in archs:
                        tmp_body.append(Ops[op](input[arch][layer]["record"][key]))
                #max_diff, max_diff_rate
                if len(lhs) == len(rhs):
                    for op in cmp_Ops: 
                        tmp_body.append(cmp_Ops[op](lhs, rhs))
                else:
                    print("Error: in"+layer + "shape of output_nv is not equal to output_bi")
                    exit(1)
    
            #params:
            tmp_body.append(input[target][layer]["nb_params"])
            total_params += input[target][layer]["nb_params"]
            if "output_shape" in hook_config["option"] and hook_config["option"]["output_shape"]:
                for o in input[target][layer]["output_shape"]:
                    total_output += np.prod(o) 
            trainable_params += input[target][layer]["nb_training_params"]
            body.append(tmp_body)
        debug_csv=pd.DataFrame(body, columns=head)
        debug_csv.to_csv(filename)
        summary_str = ""
        total_output_size = abs(2. * total_output * 4. / (1024 ** 2.))  # x2 for gradients
        total_params_size = abs(total_params * 4. / (1024 ** 2.))
        total_size = total_params_size + total_output_size

        summary_str += "Total params: {0:,}".format(total_params) + "\n"
        summary_str += "Trainable params: {0:,}".format(trainable_params) + "\n"
        summary_str += "Non-trainable params: {0:,}".format(total_params -
                                                            trainable_params) + "\n"
        summary_str += "----------------------------------------------------------------" + "\n"
        summary_str += "Forward/backward pass size (MB): %0.2f" % total_output_size + "\n"
        summary_str += "Params size (MB): %0.2f" % total_params_size + "\n"
        summary_str += "Estimated Total Size (MB): %0.2f" % total_size + "\n"
        print(summary_str)
    def draw(self, name, layers, objs):
        if len(objs) != 2:
            print("Invaild input, draw need two difference plot data")
            exit(1)
        plot1 = [objs[cmp_archs[0]][o]["record"]["output"][0].item() for o in objs[cmp_archs[0]]]
        plot2 = [objs[cmp_archs[1]][o]["record"]["output"][0].item() for o in objs[cmp_archs[1]]]
        num = len(plot1)
        nums = list(range(num + 1))[1:]
        plt.xlabel('node index')
        plt.ylabel('LOSS')
        plt.title('The ' + name + ' between  nv/bi')
        plt.plot(nums, plot1, color='red', label=cmp_archs[0])
        plt.plot(nums, plot2, color='blue', label=cmp_archs[1])
        plt.legend()
        plt.savefig("{}.jpg".format(name))
        #clear figure
        plt.clf()
    def run(self):
        #save by model's name
        #inference and backward hook
        #if not os.path.isfile(self.arch + "_" + self.name + ".npy"):
        np.save(self.arch + "_" + self.name, self.log)
        if self.if_compare:
            layers = []
            if len(self.log):
                self.arch_objs[self.arch] = self.log
            for key in archs:
                filename = key + "_" + self.name + ".npy"
                if os.path.isfile(filename) and key not in self.arch_objs: 
                    self.arch_objs[key]=np.load(filename, allow_pickle=True).item()

            for layer in self.arch_objs[cmp_archs[0]]:
                layers.append(layer)
            #in future we can use class to distingish loss and inference/bacward
            if "graph" in hook_config[self._hook_type] and hook_config[self._hook_type]["graph"]:
                self.draw("loss_" + self.name,
                          layers,
                          self.arch_objs,
                          )

            self.__compare(self.name + ".csv", 
                       self.arch_objs, 
                       layers, 
                       cmp_archs, 
                       hook_config[self._hook_type]
                       )
        for module in self.hooks:
            module.remove()

build_env=OrderedDict()
#now compare is between nv and bi
def builder(model:nn.Module, **kwargs):#arch="nv", hook_type = "inference", ignore_layers=None, persist_layers = None, if_compare=False):
    debug = hook_debug(weakref.proxy(model), **kwargs)
    build_env[debug.name] = debug
    
def run(name:str=""):
    if name == "":
        for key in build_env:
            build_env[key].run()
    else:
        build_env[name].run()

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)
        #for parm in self.parameters():
        #    torch.nn.init.normal_(parm)

    def forward(self, x=None):
        x = F.relu_(F.max_pool2d(self.conv1(x), 2))
        x = F.relu_(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = self.fc1(x)
        #x = x.copy_(x)
        x = F.relu_(x)
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        ret = F.softmax(x, dim=1)
        return F.softmax(x, dim=1)

def inference_test(platform, if_compare):
    input = torch.randn(1,1,28,28).cuda()
    model = Net().cuda()
    builder(model, arch=platform, ignore_layers=set(["conv1"]), if_compare=if_compare, name="inference")
    model.eval()
    model(input)
    run("inference")

def backward_test(platform, if_compare):
    input = torch.randn(1,1,28,28, dtype=torch.float32).cuda()
    input.requires_grad = True
    target = torch.empty(1, dtype=torch.long).random_(10).cuda()
    model = Net().cuda()
    builder(model, arch=platform, hook_type="backward", if_compare=if_compare, name="backward")
    model.train()
    criterion = torch.nn.CrossEntropyLoss()
    def train(model, input, target, epoch=10):
        optimizer = torch.optim.Adam(model.parameters(), lr = 1e-3)
        for ep in range(0, epoch):
            optimizer.zero_grad()
            output = model(input)
            loss = criterion(output, target)
            loss.backward(retain_graph=True)
            optimizer.step()
    train(model, input, target)
    run("backward")
def loss_test(platform, if_compare):
    input = torch.randn(1,1,28,28, dtype=torch.float32).cuda()
    input.requires_grad = True
    target = torch.empty(1, dtype=torch.long).random_(10).cuda()
    criterion = nn.CrossEntropyLoss()
    criterion1 = nn.CrossEntropyLoss()
    builder(criterion, arch=platform, hook_type="loss", if_compare=if_compare, name="l1")

    model = Net().cuda()
    model.train()
    def train(model, input, target, epoch=10):
        optimizer = torch.optim.Adam(model.parameters(), lr = 1e-3)
        for ep in range(0, epoch):
            optimizer.zero_grad()
            output = model(input)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
    train(model, input, target)
    run("l1")

def test_parser():
    parser = argparse.ArgumentParser(description='PyTorch Debug Test')
    parser.add_argument('--inference','-i', action="store_true", help='test inference')
    parser.add_argument('--backward','-b', action="store_true", help='test backward')
    parser.add_argument('--loss','-l', action="store_true", help='test loss')
    parser.add_argument('--platform','-p', default="nv", type=str, help='test on nv or bi')
    parser.add_argument('--if_compare','-c', action="store_true", help='if_compare')
    args = parser.parse_args()
    #set_fullbackward()
    
    if args.inference:
        inference_test(args.platform, args.if_compare)
    
    if args.backward:
        backward_test(args.platform, args.if_compare)
    
    
    if args.loss:
        loss_test(args.platform, args.if_compare)

# test_parser()





