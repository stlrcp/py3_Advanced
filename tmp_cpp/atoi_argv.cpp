#include <iostream>
#include <cstdlib>
using namespace std;

void compare(int a, int b){
    try {
        if (a > b){
            throw std::runtime_error(" a > b, this is a compare error!!!");
        }
    } catch(const std::runtime_error& e){
        std::cerr << "捕获到异常: " << e.what() << ' ';
    }
}

int main(int argc, char **argv){
    int n = atoi(argv[1]);
    int c = atoi(argv[2]);
    std::string file;
    int line;
    cout << "n = " << n << endl;
    cout << "c = " << c << endl;
    cout << "file = " << __FILE__ << " line = " << __LINE__ << endl;
    cout << "file = " << file << " line = " << line << endl;
    // std::runtime_error("this is a error");
    compare(n, c);
    return 0;
}
