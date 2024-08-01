#include <torch/torch.h>
#include <iostream>

int main() {
    if (torch::cuda::is_available()) {
        std::cout << "CUDA is available! Running on GPU." << std::endl;
        // 创建一个随机张量并将其移到GPU上
        torch::Tensor tensor_gpu = torch::rand({2, 3}).cuda();
        std::cout << "Tensor on GPU:\n" << tensor_gpu << std::endl;
    } else {
        std::cout << "CUDA not available! Running on CPU." << std::endl;
        // 创建一个随机张量并保持在CPU上
        torch::Tensor tensor_cpu = torch::rand({2, 3});
        std::cout << "Tensor on CPU:\n" << tensor_cpu << std::endl;
    }
    return 0;
}
