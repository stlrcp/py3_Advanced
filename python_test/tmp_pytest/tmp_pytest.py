import pytest

# class Test_Case:
#     t = 0
#     def test_c(self):
#         self.t = self.t + 1
#         assert self.t == 1
#     def test_d(self):
#         self.t = self.t + 1
#         assert self.t == 1
        
# s = {}
# class Test_Case:
#     def test_b(self):
#         global s
#         s['name'] = 'hello'
#         print(s['name'])
#         assert s['name'] == 'hello'
#     def test_c(self):
#         global s 
#         s['age'] = 18
#         print(s)
#         assert s['age'] == 18
# # global 声明的变量可以在整个测试类中共享，值是可变的，global可以去掉，效果相同

# @pytest.mark.parametrize()

# class Test_Case:
#     @pytest.mark.parametrize('x', [1, 2, 3, 4])   # 传递单个值
#     def test_b(self, x):
#         assert x != 5
        
#     @pytest.mark.parametrize("x, y", [(1,2), (3, 4), (2, 3), (4,6)])  # 多参数，传递元组
#     def test_c(self, x, y):
#         print(x + y)
#         assert x+y != 5
        
#     @pytest.mark.parametrize("x, y", [{1,2}, {3,4}, {2,3}, {4, 6}])  # 多参数传递集合
#     def test_d(self, x, y):
#         print(x+y)
#         assert x+y != 6
        
#     @pytest.mark.parametrize("x", [{"a": 1, "b": 2}, {"a":1, "c": 4}])  # 传递字典
#     def test_e(self, x):
#         print(x)
#         assert x["a"] == 1
        
#     @pytest.mark.parametrize("x, y", [({"a": 1, "b":2}, {"a":3, "c":4})])   # 多参数传递字典
#     def test_f(self, x, y):
#         assert x["a"] == 1
        
#     @pytest.mark.parametrize("test_input, expected",
#                              [("3+5", 8), ("2+4", 6), pytest.param("6*9", 42, marks=pytest.mark.xfail)],)  # xfail 标记
#     def test_h(self, test_input, expected):
#         assert eval(test_input) == expected
        
#     @pytest.mark.parametrize("test_input, expected", 
#                              [("3+5", 8), ("2+4", 6), pytest.param("6*9", 42, marks=pytest.mark.skip)],)  # skip 标记
#     def test_i(self, test_input, expected):
#         assert eval(test_input) == expected


# # fixtrue 传递
# import pytest
# class Test_Case:
#     @pytest.fixture
#     def get_d(self):   # 通过fixture值传递
#         return [1,2,3]
#     def test_a(self, get_d):
#         x = get_d[0]
#         assert x == 1


# import pytest
# class Test_Case:
#     # params = "hello" 等同于 params = ['h', 'e', 'l', 'l', 'o']
#     @pytest.fixture(params='hello')
#     def get_c(self, request):
#         print(request.param)
#         return request.param
    
#     def test_c(self, get_c):
#         name = get_c
#         assert name == 'h'
        
#     @pytest.fixture(params=[1, 2], ids=['hello', 'name'])    # 可以通过 pytest -k <ids> 执行指定的用例
#     def get_d(self, request):
#         return request.param
    
#     def test_d(self, get_d):
#         name = get_d
#         assert name == 2
        
#     @pytest.fixture(params=[0, 1, pytest.param(2, marks=pytest.mark.skip)])
#     def data_set(self, request):
#         return request.param 
    
#     def test_f(self):
#         pass


# import pytest
# # fixture 嵌套传递
# class Test_Case:
#     @pytest.fixture(params=[0, 1, pytest.param(2, marks=pytest.mark.skip)])
#     def data_set(self, request):
#         return request.param 
    
#     @pytest.fixture()
#     def data_s(self, data_set):
#         print(data_set)
#         return data_set
    
#     def test_g(self, data_s):
#         assert data_s == 1
    

# # yield 传递
# import pytest
# class Test_Case:
#     @pytest.fixture
#     def s(self):
#         c = 'test'
#         yield c 
        
#     def test_name(self, s):
#         assert s == "test"
        
        
# # 配置文件传递
# import pytest
# import _case.constant as d 

# class Test_Case:
#     def test_g(self):
#         d.data = 2
#         assert d.data == 2
        
#     def test_h(self):
#         assert d.data == 2
# # # _case.constant.py
# # data = 1
# # 和 global 使用类似，多个测试文件共享值，但是多个文件共享该值时，会受到测试文件的执行顺序影响
# # global 只能在一个测试文件中共享值


# # conftest.py 最好是在项目根目录或者测试文件所在目录
# import pytest
# @pytest.fixture(scope='session')
# def say():
#     return 'hello'

# import pytest
# class Test_Case:
#     def test_g(self, say):
#         assert say == 'hello'


# # # conftest.py   全局变量使用
# # import pytest
 
# # def pytest_addoption(parser):
# #     parser.addoption("--file", default="test")
 
# # @pytest.fixture
# # def file_name(request):
# #     return request.config.getoption("--file")

# import pytest
# class Test_Case:
#     def test_name(self, file_name):
#         assert file_name == "test"
#     # test_case.py 或者直接在测试文件中通过 pytestconfig 获取，示例如下
#     def test_name(self, pytestconfig):
#         print(pytestconfig.getoption('file'))
#         assert pytestconfig.getoption("file") == "test"


# # 钩子函数传参
# # conftest.py
# import pytest
# def pytest_addoption(parser):
#     parser.addoption("--file", default="test")
# def pytest_generate_tests(metafunc):
#     file = metafunc.config.getoption('--file')
#     metafunc.parametrize("case_data", [file])

# import pytest
# class Test_Case:
#     def test_g(self, case_data):
#         assert case_data == 'test'


# # 复制
# # conftest.py
# import pytest
# def pytest_addoption(parser):
#     parser.addoption("--file", default="test")
    
# def pytest_generate_tests(metafunc):
#     file = metafunc.config.getoption("--file")
#     metafunc.parametrize("case_data", [file])

# test_case.py
import pytest 

class Test_Case:
    def test_g(self, case_data):
        assert case_data == 'test'
    
