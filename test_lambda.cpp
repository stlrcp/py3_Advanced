/*
// C++ 中的 lambda 表达式  -  https://blog.csdn.net/qq_28368377/article/details/123928998
// lambda 表达式会被编译器翻译成类进行处理
// lambda 表达式的基本组成部分
//   -- [捕获]（参数）说明符 -> 返回类型 {函数体}
//   1. 最简单的 lambda 表达式：
//     -- []{};
//     只需要函数体的[], 然后函数体为空{}. 参数列表()是可选的。
//   2. 带两个参数的 lambda 表达式：
//     -- [](float f, int a) {return a * f;};
//     -- [](int a, int b) {return a < b;};
//     不需要返回类型，因为编译器将自动推导它。
//   3. 箭头+类型表示返回类型：
//     -- [](MyClass t) -> int {auto a = t.compute(); print(a); return a;};
//     箭头+类型表示返回类型也可用于常规函数声明。
#include <iostream>
int main() {
    int x = 8;
    auto l1 = []<typename T>(T val)
    {
        return val + 10;
    };
    const int y = l1(10);
    std::cout << y << std::endl;
}
// lambda表达式打印输出
#include <algorithm>
#include <iostream>
#include <vector>
void PrintFunc(int x){
    std::cout << x << " ";
}
int main(){
    std::vector<int> x = {1, 2, 3, 4};
    std::for_each(x.begin(), x.end(), PrintFunc);
    std::cout << "\nlambda: " << std::endl;
    std::for_each(x.begin(), x.end(), [](int x)
                  { std::cout << x << " "; });
    return 0;
}

// std::function 与 lambda 比较
#include <iostream>
#include <functional>
int main(){
    const auto myLambda = [](int a) noexcept -> double
    {
        return 2.0 * a;
    };
    const std::function<double(int)> myFunc = [](int a) noexcept -> double
    { return 2.0 * a; };
    std::cout << "Sizeof(myLambda) is : " << sizeof(myLambda) << std::endl;
    std::cout << "Sizeof(myFunc) is : " << sizeof(myFunc) << std::endl;
    std::cout << "myFunc(10) = " << myFunc(10) << std::endl;
    std::cout << "myLambda(10) = " << myLambda(10) << std::endl;
    return myFunc(10) == myLambda(10);
}

// 复制一个 Lambda
#include <iostream>
#include <type_traits>
int main(){
    const auto my1Lambda = [](int a) noexcept
    { return 2.0 * a; };
    const auto my2Lambda = my1Lambda;
    std::cout << std::is_same<decltype(my1Lambda), decltype(my2Lambda)>::value << std::endl;
}

// 捕获
#include <iostream>
int main() {
    int x = 2, y = 3;
    const auto l1 = []() {return 1;};   // 无捕获
    const auto l2 = [=]() {return x;};   // 所有值捕获
    const auto l3 = [&]() {return y;};    // 所有引用捕获
    const auto l4 = [x]() {return x;};    // x 值捕获
    const auto l5 = [&y]() {return y;};    // y引用捕获
    const auto l6 = [x, &y]() {return x * y;};   // x值捕获，y引用捕获
    const auto l7 = [=, &x]() {return x + y;};    // x引用捕获，其他值捕获
    const auto l8 = [&, y]() {return x - y;};    // y值捕获，其他引用捕获
    std::cout << l1 << std::endl;
}

// this 使用
#include <iostream>
#include <functional>
struct Str{
    auto func(){
        int val = 1;
        auto mylambda = [val, this]()
        {
            std::cout << x << std::endl;
            return val > x;
        };
        return mylambda();
    }
    int x = 10;
};
int main(){
    Str s;
    s.func();
    // std::cout << s.func() << std::endl;
}

// 捕获初始化
#include <iostream>
#include <functional>
int main(){
    int x = 8;
    auto l1 = [y = x](int val)
    {
        std::cout << "y = " << y << std::endl;
        return val > y;
    };
    std::cout << l1(10) << std::endl;
}

// 使用 constexpr, 可在编译期执行
#include <iostream>
int main(){
    int x = 8;
    auto l1 = [](int val) constexpr
    {
        return val + 10;
    };
    constexpr int y = l1(10);
    std::cout << y << std::endl;
}  // g++ -std=c++1z test_lambda.cpp


// lambda 表达式的深入应用
// 捕获时计算
#include <iostream>
int main(){
    int x = 8, y = 10;
    auto l1 = [z = x + y]()
    {
        return z;
    };
    std::cout << l1() << std::endl;
}

// 即调用函数表达式
#include <iostream>
int main(){
    int x = 8, y = 10;
    auto l1 = [z = x + y]()
    {
        return z;
    }();
    std::cout << l1 << std::endl;
} // 即调用函数表达式：先创建 Lambda 表达式，并不分配给任何闭包对象，然后它被()调用。

// 生成 html
#include <iostream>
#include <string>
void ValidateHTML(const std::string&) {}
std::string BuildAHref(const std::string& link, const std::string& text){
    const std::string html = [&link, &text]
    {
        const auto &inText = text.empty() ? link : text;
        return "<a href= \" " + link + " \" >" + inText + "</a>\n";
    }(); // call!
    ValidateHTML(html);
    return html;
}
 int main(){
    try {
        const auto ahref = BuildAHref("www.leanpub.com", "Leanpub Store");
        std::cout << ahref;
    }
    catch (...) {
        std::cout << "bad format...";
    }
 }

// 使用 auto 避免复制
#include <iostream>
int main(){
    int x = 8;
    auto l1 = [](auto a)
    {
        return ++a;
    };
    std::cout << l1(x) << std::endl;
}

// 实现 map 中 键值求和
#include <iostream>
#include <functional>
#include <algorithm>
#include <map>
void PrintFunc(int x){
    std::cout << x << " ";
}
int main(){
    std::map<int, int> m{{1, 2}, {3, 4}, {4, 5}, {5, 6}};
    auto lam = [](const auto &p) // auto表示 std::pair<const int, int>
    {
        return p.first + p.second;
    };
    std::vector<int> v;
    for (auto &i : m){
        v.push_back(lam(i));
    }
    std::for_each(v.cbegin(), v.cend(), PrintFunc);
    return 0;
}

// lambda 实现函数重载 （Lifting）
#include <iostream>
auto fun(int val){
    return val + 10;
}
auto fun(double val){
    return val + 12.0;
}
int main(){
    auto lam = [](auto x)
    {
        return fun(x);
    };
    std::cout << lam(1) << std::endl;
}

// 求 n 的阶乘（递归调用）
#include <iostream>
int factorial(int n){
    return n > 1 ? n * factorial(n - 1) : 1;
}
int main(){
    auto factorial1 = [](int n)
    {
        auto f_impl = [](int n, const auto &impl) -> int
        {
            return n > 1 ? n * impl(n - 1, impl) : 1;
        };
        return f_impl(n, f_impl);
    };
    std::cout << factorial(10) << std::endl;
    std::cout << factorial1(10) << std::endl;
}


// AI 编译优化技术 "loop tiling"、"ordering"、"caching"、"unrolling" -- https://blog.csdn.net/qq_47564006/article/details/134674673
// Loop Tiling (循环平铺)
// 循环平铺是一种循环变换技术，用于优化多维循环的性能，这通常在处理大型数组或矩阵时很有用。目的是将大循环分解成"块"或"瓦片"，使得每个小块的数据能够有效地放入
// CPU缓存中，从而减少对主存储器的访问次数。这有助于提高局部性，因为缓存比主内存有更快的访问速度。
#include <iostream>
#define N 1024
double A[N][N], B[N][N], C[N][N];
// void matrix_multiply(double (&A)[1024][1024], double (&B)[1024][1024], double (&C)[1024][1024]){
void matrix_multiply(){
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            C[i][j] = 0;
            for (int k = 0; k < N; k++){
                C[i][j] += A[i][k] * B[k][j];
                // C[i][j] = A[i][k] * B[k][j];
            }
        }
    }
}
//  应用循环平铺的版本
#define TILE_SIZE 32   // 假设这是一个合适的平铺大小
void tiled_matrix_multiply(){
    for (int i = 0; i < N; i+= TILE_SIZE){
        for (int j = 0; j < N; j+= TILE_SIZE){
            for (int k = 0; k < N; k+= TILE_SIZE){
                for (int ii = i; ii < i + TILE_SIZE; ii++){
                    for (int jj = j; jj<j+TILE_SIZE; jj++){
                        for (int kk = k; kk < k + TILE_SIZE; kk++){
                            C[ii][jj] += A[ii][kk] * B[kk][jj];
                        }
                    }
                }
            }
        }
    }
}
int main(){
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            A[i][j] = 1;
            B[i][j] = 2;
        }
    }
    // matrix_multiply(A, B, C);
    // matrix_multiply();
    tiled_matrix_multiply();
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++){
            printf("C[%d][%d] = %lf \n", i, j, C[i][j]);
        }
    }
    // for (int i = 0; i < N; i += TILE_SIZE){
    //     printf("i =============== %d\n", i);
    //     for (int ii = i; ii < i + TILE_SIZE; ii++)
    //     {
    //         printf("ii = %d \n", ii);
    //     }
    // }
        return 0;
}


// Ordering(顺序)：
// 访问二维数组时，行优先和列优先的访问方式对性能有很大影响。假定一个简单的二维数组求和：
// 编程中的循环顺序是指嵌套循环访问数据的顺序。例如，在二维数组中，你可以先按行（row-major order）访问，也可以先按列（column-major order）访问。
// 选择正确的循环顺序可以增加程序的缓存命中率。从而提高性能。
#include <iostream>
#include <time.h>
#define N 1024
double A[N][N];
// 行优先访问
double sum_row_major(){
    double sum = 0;
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            sum += A[i][j];
        }
    }
    return sum;
}
// 列优先访问
double sum_column_major(){
    double sum = 0;
    for (int j = 0; j < N; j++){
        for (int i = 0; i < N; i++){
            sum += A[i][j];
        }
    }
    return sum;
}
int main(){
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            A[i][j] = 1;
        }
    }
    clock_t begin, end;
    double cost, sum;
    begin = clock();
    sum = sum_row_major();
    end = clock();
    cost = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("constant CLOCKS_PER_SEC is: %ld, sum_row_major time cost is: %lf secs, sum = %lf \n", CLOCKS_PER_SEC, cost, sum);
    begin = clock();
    sum = sum_column_major();
    end = clock();
    cost = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("constant CLOCKS_PER_SEC is: %ld, sum_column_major time cost is: %lf secs, sum = %lf \n", CLOCKS_PER_SEC, cost, sum);
}


// Caching(缓存)：
// 在编程中，缓存是一种保存数据副本的技术，目的是在后续访问时可以更快地获取数据。在循环优化中，考虑如何有效使用 CPU 的缓存及其重要，
// 因为存储器访问是影响性能的关键因素之一。合理的缓存使用可以显著减少从主内存中加载数据的次数，因为内存访问比缓存访问的成本要高得多。
// 使用缓存来提高数据访问速度得一个例子可能是计算 斐波那契数列，用一个数组来缓存以前计算得结果：
# 斐波那契数列的缓存实现：
def fibonacci(n, cache={}):
    if n in cache:
        return cache[n]
    if n <= 1:
        return n 
    else:
        cache[n] = fibonacci(n-1, cache) + fibonacci(n-2, cache)
        return cache[n]
# 可以这样使用
print(fibonacci(50))  # 非常快速地计算出结果


// Unrolling(展开)：
// 循环展开是一种编译器优化技术，它通过减少循环迭代的次数来减少循环控制开销。通过将一个循环的多个迭代合并为一个迭代里面的多个连续操作，
// 可以减少循环维护（比如递增计数器和条件跳转）的次数。循环展开可以增加程序的大小，但通常能减少执行时间，特别是在循环的迭代次数非常多的时候。
// 下面是一个简单的循环展开例子，展开后的循环可以减少循环迭代的次数：
#include <iostream>
#include <time.h>
#define N 1024
double A[N];
// 未展开的循环
double sum_array(){
    double sum = 0;
    for (int i = 0; i < N; i++){
        sum += A[i];
    }
    return sum;
}
// 展开的循环
double sum_array_unrolled(){
    double sum = 0;
    for (int i = 0; i < N; i += 4){   // 一次处理4个元素
        sum += A[i] + A[i + 1] + A[i + 2] + A[i + 3];
    }
    return sum;
}
int main(){
    for (int i = 0; i < N; i++){
        A[i] = 1;
    }
    clock_t begin, end;
    double cost, sum;
    begin = clock();
    sum = sum_array();
    end = clock();
    cost = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("CLOCKS_PER_SEC = %ld, sum_array time cost = %lf secs, sum = %lf \n", CLOCKS_PER_SEC, cost, sum);
    begin = clock();
    sum = sum_array_unrolled();
    end = clock();
    cost = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("CLOCKS_PER_SEC = %ld, sum_array_unrolled time cost = %lf secs, sum = %lf \n", CLOCKS_PER_SEC, cost, sum);
}
*/
