"""
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
"""

"""
# 为函数添加一个统计运行时长的功能  ####   一般写法
import time
import threading
def how_much_time(func):
    def inner():
        t_start = time.time()
        func()
        t_end = time.time()
        print("一共花费了{0}秒时间".format(t_end - t_start))
    return inner
    # 将增加的新功能代码以及被装饰函数运行代码func()一同打包返回，返回的是一个内部函数，这个被返回的函数就是装饰器
def sleep_5s():
    time.sleep(5)
    print("%d秒结束了" % (5,))
def sleep_6s():
    time.sleep(6)
    print("%d秒结束了" % (6,))
sleep_5s = how_much_time(sleep_5s)
# 因为sleep_5s函数的功能就是睡5秒钟，虽然增加了统计运行时间的功能，但是他本身功能没变(还是睡5秒钟)，所以仍然用原来函数名接收增加功能了的自己
sleep_6s = how_much_time(sleep_6s)
t1 = threading.Thread(target=sleep_5s)
t2 = threading.Thread(target=sleep_6s)
t1.start()
t2.start()


## 为函数添加一个统计运行时长的功能  #### 标准的语法糖写法
import time
import threading
def how_much_time(func):
    def inner():
        t_start = time.time()
        func()
        t_end = time.time()
        print("一共花费了{0}秒时间".format(t_end - t_start))
    return inner
@how_much_time
# @how_much_time 等价于 sleep_5s = how_much_time(sleep_5s)
def sleep_5s():
    time.sleep(5)
    print("%d秒结束了" % (5,))
@how_much_time
def sleep_6s():
    time.sleep(6)
    print("%d秒结束了" % (6,))
t1 = threading.Thread(target=sleep_5s)
t2 = threading.Thread(target=sleep_6s)
t1.start()
t2.start()


# 为函数添加一个统计时长的功能以及日志记录功能   ##### 给某个函数加上多个装饰器
import time
import threading
def how_much_time(func):
    print("how_much_time函数开始了")
    def inner():
        t_start = time.time()
        func()
        t_end = time.time()
        print("一共花费了{0}秒时间".format(t_end-t_start))
    return inner
def mylog(func):
    print("mylog函数开始了")
    def inner_1():
        print("start")
        func()
        print("end")
    return inner_1
@mylog
@how_much_time
# 等价于 mylog(how_much_time(sleep_5s))
def sleep_5s():
    time.sleep(5)
    print("%d秒结束了" % (5,))
if __name__ == "__main__":
    sleep_5s()
# 执行顺序是：
# 1. 第一步先执行how_much_time函数的外部代码；
# 2. 第二步执行mylog函数的外部代码；
# 3. 第三步执行mylog的内部函数代码；
# 4. 第四步执行how_much_time函数的内部函数代码；


# 带参数的装饰器的典型写法
def mylog(type):
    # 带参数装饰器的典型写法，对下面装饰器再进行一次嵌套
    def decorator(func):
        # 装饰器，如果这个装饰器需要参数，需要在外面再嵌套一个函数，参数写在外面函数里面
        def infunc(*args, **kwargs):
            if type == "文件":
                print("文件中：日志记录")
            else:
                print("控制台：日志记录")
            return func(*args, **kwargs)
        return infunc
    return decorator
@mylog("文件")
# 采用语法糖格式生成的装饰器，参数写在@mylog里面，也就是写在新加的外层函数里面
def fun2(a, b):
    print("使用功能2", a, b)
if __name__ == '__main__':
    fun2(100, 200)


# @wraps()语法糖(了解)   #### wraps装饰器案例
from functools import wraps
# 从functool包导入wraps，functool是python函数式编程的核心包
def mylog(func):
    @wraps(func)
    ## wraps()写在这个地方，因为他修饰内部函数，保证这个内部函数带有传进来这个函数的属性
    def infunc(*args, **kwargs):
        print("日志记录...")
        print("函数文档: ", func.__doc__)
        return func(*args, **kwargs)
    return infunc
@mylog   # fun2 = mylog(fun2)
def fun2():
    ### 强大的功能2 ###
    print("使用功能2")
if __name__ == "__main__":
    fun2()
    print("函数文档--->", fun2.__doc__)


# 类装饰器
# 类装饰器的写法，主要思路就是返回一个增加了新功能的函数对象，只不过这个函数对象是一个类的实例对象
# 由于装饰器是可调用对象，所以必须在类里面实现__call__方法
### 不带参数的类装饰器
import time
class Decorator:
    def __init__(self, func):
        self.func = func
    def defer_time(self):
        time.sleep(5)
        print("延时结束了")
    def __call__(self, *args, **kwargs):
        start_time = time.time()
        self.defer_time()
        self.func()
        end_time = time.time()
        print("执行时间为：", end_time - start_time)
@Decorator
def f1():
    print("延时之后我才开始执行")
f1()


## 带参数的类装饰器
import time
class Decorator:
    def __init__(self, func):
        self.func = func
    def defer_time(self, time_sec):
        time.sleep(time_sec)
        print(f"{time_sec}s延时结束了")
    def __call__(self, time):
        self.defer_time(time)
        self.func()
@Decorator
def f1():   ### () 不带参数
    print("延时之后我才开始执行")
f1(5)   ### 实际参数5会被传到__call__方法这里，并将实参5赋给形参time
"""

## python中的装饰器(decorator)是一个接受另一个函数作为参数的函数
# 装饰器通常会修改或增强它接受的函数并返回修改后的函数
# 装饰器不仅可以是函数，还可以是类。使用类装饰器主要依靠类的__call__方法，一个函数可以同时定义多个装饰器
# python自带几个内置装饰器：@classmethod; @staticmethod; @property
import functools
var = 8
def another_function(func):
    ### A function that accepts another function ###
    def other_func():  # 嵌套函数
        val = "The result of %s is %s" % (func(), eval(func()))
        return val
    return other_func
if var == 1:
    # reference: https://python101.pythonlibrary.org/chapter25_decorators.html
    def a_function():
        ### A pretty useless function ###
        return "1+1"
    value = a_function()
    print(value)
    decorator = another_function(a_function)
    print(decorator())
elif var == 2:
    # 对以上示例做些修改，加入装饰器 https:://python101.pythonlibrary.org/chapter25_decorators.html
    @another_function    ## 这里的@称为语法糖
    def a_function():
        ### A pretty useless function ###
        return "1+1"
    value = a_function()
    print(value)
elif var == 3:
    # reference: http://python101.pythonlibbrary.org/charter25_decorators.html
    class DecoratorTest(object):
        ### Test regular method vs @classmethod vs @staticmethod ###
        def __init__(self):
            ### Constructor ###
            pass
        def doubler(self, x):
            print("running doubler")
            return x*2
        @classmethod ## 可以使用类的实例或直接由类本身作为其第一个参数来调用
        def class_tripler(klass, x):
            print("running tripler: %s" % klass)
            return x*3
        @staticmethod  ## 类中的一个函数，可以在实例化类或不实例化类的情况下调用它
        def static_quad(x):
            print("running quad")
            return x*4
    decor = DecoratorTest()
    print(decor.doubler(5))
    print(decor.class_tripler(3))
    print(DecoratorTest.class_tripler(3))
    print(DecoratorTest.static_quad(2))
    print(decor.static_quad(3))
    print(decor.doubler)
    print(decor.class_tripler)
    print(decor.static_quad)
elif var == 4:
    # https://python101.pythonlibrary.org/chapter25_decorators.html
    class Person(object):
        def __init__(self, first_name, last_name):
            ### Constructor ###
            self.first_name = first_name
            self.last_name = last_name
        @property  ## 将类方法转换为属性
        def full_name(self):
            ### Return the full name ###
            return "%s %s" % (self.first_name, self.last_name)
    person = Person("Mike", "Driscoll")
    print(person.full_name)  # 注意: person.full_name 与 person.full_name()区别
    print(person.first_name)
    # person.full_name = "Jackalope" # attributeError: can't set attribute, 不能将属性设置为不同的值，只能间接进行
    person.first_name = "Dan"
    print(person.full_name)
elif var == 5:
    # reference: https://www.geeksforgeeks.org/decorators-in-python/
    def shout(text):
        return text.upper()
    yell = shout # assign the function shout to a variable
    print(yell('Hello'))
    def greet(func):   # greet function takes another function as a parameter
        greeting = func("Hi, I am created by a function passed as an argument.")  # storing the function in a variable
        print(greeting)
    greet(shout)
    def create_adder(x):
        def adder(y):
            return x+y
        return adder  # function can return another function
    add_15 = create_adder(15)
    print(add_15(10))
elif var == 6:
    # reference: https://www.geeksforgeeks.org/decorators-in-python/
    def hello_decorator(func):   # defining a decorator
        # inner is a Wrapper function in which the argument is called
        # inner function can access the outer local functions like in this case "func"
        @functools.wraps(func)  # 内置装饰器@functools.wraps会保留原函数的元信息，将元信息拷贝到装饰器里面的func函数中
        def inner():
            print("Hello, this is before function execution:", func.__name__) # 函数对象的__name__属性，可以拿到函数的名字
            func()  # calling the actual function now inside the wrapper function
            print("This is after function execution")
        return inner
    # defining a function, to be called inside wrapper
    def function_to_be_used():
        print("This is inside the function !!")
    print("decorator before, function name: ", function_to_be_used.__name__)
    function_to_be_used()  # 装饰器前
    # passing 'function_to_be_sued' inside the decorator to control its behavior
    function_to_be_used = hello_decorator(function_to_be_used)
    # 注意：如果上面inner函数定义前不加@functools.wraps, 下面的print将输出inner，添加后会输出function_to_be_sued
    print("decorator after, function name:", function_to_be_used.__name__)
    function_to_be_used()   # 装饰器后
    # above code is equivalent to
    print("==================")
    @hello_decorator
    def function_to_be_used2():
        print("This is inside the function !!")
    function_to_be_used2()
elif var == 7:
    # reference: https://www.geeksforgeeks.org/decorators-in-python/
    def hello_decorator(func):
        # The inner function takes the argument as *args and **kwargs which means
        # that a tuple of positional arguments or a dictionary of keyword arguments can be passed of any length
        # This makes it a general decorator that can decorate a function having any number of arguments
        @functools.wraps(func)
        def inner(*args, **kwargs): # *args表示所有的位置参数，**kwargs表示所有的关键字参数，之后再将其传到func函数中，这样保证了能完全传递所有参数
            print("before Execution")
            print("call function:", func.__name__)
            returned_value = func(*args, **kwargs)  # getting the returned value
            print("after Execution")
            return returned_value   # returning the value to the original frame
        return inner
    # adding decorator to the function
    @hello_decorator
    def sum_two_numbers(a, b):
        print("Inside the function")
        return a + b
    a, b = 1, 2
    # getting the value through return of the function
    print("Sum =", sum_two_numbers(a, b))
elif var == 8:
    class decorator:
        def __init__(self, func):
            self.func = func
        def __call__(self, *args, **kwargs):
            print("function name:", self.func.__name__)
            return self.func(*args, **kwargs)
    @decorator
    def add(a, b):
        print("add value:", a+b)
    add(2, 3)
print("test finish")










