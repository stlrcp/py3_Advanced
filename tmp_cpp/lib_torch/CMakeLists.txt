cmake_minimum_required(VERSION 3.10 FATAL_ERROR)
project(test_project)

# Setting the C++ standard to C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# If additional compiler flags are needed
add_compile_options(-Wall -Wextra -pedantic)

# Setting the location of LibTorch
set(Torch_DIR "/usr/local/lib64/python3.10/site-packages/torch/lib/")
find_package(Torch REQUIRED)

# Specify the name of the executable and the corresponding source file
add_executable(test_project main.cpp)

# Linking LibTorch libraries
target_link_libraries(test_project "${TORCH_LIBRARIES}")

# Set the output directory for the executable
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
