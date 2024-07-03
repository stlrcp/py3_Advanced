# import pytest

# @pytest.fixture(scope='session')
# def say():
#     return 'hello'


# import pytest

# def pytest_addoption(parser):
#     parser.addoption("--file", default="test")
    
# @pytest.fixture
# def file_name(request):
#     return request.config.getoption("--file")


# import pytest
# def pytest_addoption(parser):
#     parser.addoption("--file", default="test")
# def pytest_generate_tests(metafunc):
#     file = metafunc.config.getoption('--file')
#     metafunc.parametrize("case_data", [file])


import pytest
def pytest_addoption(parser):
    parser.addoption("--file", default="test")
    
def pytest_generate_tests(metafunc):
    file = metafunc.config.getoption("--file")
    metafunc.parametrize("case_data", [file])
