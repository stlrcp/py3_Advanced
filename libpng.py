# import cv2
# from skimage import io
# path = r"C:\迅雷下载\train\100.jpg"
# image = io.imread(path)
# print(image.shape)
# image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
# print(image.shape)
# cv2.imencode('.png', image)[1].tofile(path)
# print(len(cv2.imencode('.png', image)[1]))



# import os
# from tqdm import tqdm
# import cv2
# from skimage import io
# path = r"C:\迅雷下载\train"
# filelist = os.listdir(path)
# # print(filelist)
# for i in tqdm(filelist):
#     image = io.imread(path+"\\"+i)   # image = io.imread(os.path.join(path, i))
#     image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
#     cv2.imencode('.png', image)[1].tofile(path+"\\"+i)



# 构建计算图 - 简单实现自动求导
import numpy as np 
class Variable:
    def __init__(self, value=None):
        self.value = value
        self.grad = None
        self.next = None
        self.root = None
    def func(x):
        return
    def func_grad(x):
        return
class placeholder(Variable):
    def __init__(self, size):
        super().__init__(self)  # 运行父类的构造函数
        self.size = size
        self.root = self   # root 就是自己
        self.grad = 1
class exp(Variable):
    def __init__(self, x):
        super().__init__()  # 继承父类
        x.next = self  # 作为上一个节点的下一步运算
        self.root = x.root  # 声明自变量，复合函数自变量都是前一函数的自变量
    def func(self, x):
        return np.exp(x)
    def func_grad(self, x):
        return np.exp(x)
class sin(Variable):
    def __init__(self, x):
        super().__init__()
        x.next = self
        self.root = x.root
    def func(self, x):
        return np.sin(x)
    def func_grad(self, x):
        return np.cos(x)
class cos(Variable):
    def __init__(self, x):
        super().__init__()
        x.next = self
        self.root = x.root
    def func(self, x):
        return np.cos(x)
    def func_grad(self, x):
        return -np.sin(x)
class log(Variable):
    def __init__(self, x):
        super().__init__()
        x.next = self
        self.root = x.root
    def func(self, x):
        return np.log(x)
    def func_grad(self, x):
        return 1 / x
class square(Variable):
    def __init__(self, x):
        super().__init__()
        x.next = self
        self.root = x.root
    def func(self, x):
        return np.square(x)
    def func_grad(self, x):
        return 2 * x
class Session:
    def run(self, operator, feed_dict):
        root = operator.root  # 计算起始点
        root.value = feed_dict[root]   # 传入自变量的数据
        while root.next is not operator.next: #  计算到operator便停止计算
            root.next.value = root.next.func(root.value)   # 计算节点的值
            root.next.grad = root.grad * root.next.func_grad(root.value)  # 计算梯度
            root = root.next  # 去往下一个节点
        return root.value
xs = placeholder((2, 2))
h1 = square(xs)
h2 = log(h1)
h3 = sin(h2)
h4 = exp(h3)
# 具体数据
x = np.array([[1, 2], [3, 4]])
# 建立 Session 计算
sess = Session()
out = sess.run(h4, feed_dict = {xs: x})
# 自动求导
grad = h4.grad
# 手动求导
grad0 = np.exp(np.sin(np.log(np.square(x)))) * np.cos(np.log(np.square(x))) * 1/np.square(x) * 2 * x 
print()
print("自动求导：\n", grad)
print("手动求导：\n", grad0)
