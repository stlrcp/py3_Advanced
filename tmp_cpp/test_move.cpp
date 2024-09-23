//   https://zhuanlan.zhihu.com/p/645258818
// std::move 是 C++ 标准库中的一个 函数模板，用于将一个左值（左值引用）转化为右值引用，从而实现移动语义。
// 移动语义是一种可以将资源（如内存）从一个对象转移到另一个对象的方式，而不是进行资源的复制。
// 移动操作通常比复制操作更高效，对于大型的对象（如容器、字符串等）可以带来很大的性能优势。

// 左值和右值
// 在C++中，左值是可以被取地址的表达式，而右值是临时的、不可取地址的表达式。
// 通常，左值是具有名称、有持久性的，而右值是临时性的、瞬时的。其具体区别如下：
// 1. 左值是可以放在赋值号左边可以被赋值的值；左值必须要在内存中有实体。
// 2. 右值是在赋值号右边取出值赋给其他变量的值；右值可以在内存也可以在 CPU 寄存器。
// 3. 一个对象被用作右值时，使用的是它的内容（值），被当作左值时，使用的是它的地址。
// 4. 左值：指表达式结束后依然存在的持久对象，可以取地址，具名变量或对象。
// 5. 右值：表达式结束后就不再存在的临时对象，不可以取地址，没有名字。

// 使用 std::move 可以告诉编译器将一个对象视为右值，从而触发移动语义的操作。

#include <stdio.h>
#include <unistd.h>
#include <iostream>
#include <vector>

class MyClass{
    public:
        MyClass(int value): ptr_(new int(value)){
            // 构造函数，存在开辟内存，复制资源的操作
            std::cout << "Default constructor called: MyClass(int value)" << ptr_ << std::endl;
        }
        MyClass(const MyClass& other) : ptr_(new int(*other.ptr_)){
            // 拷贝构造函数，存在开辟内存，复制资源的操作
            std::cout << "Copy constructor called: MyClass(const Myclass& other)" << other.ptr_ << std::endl;
        }
        MyClass(MyClass&& other) noexcept : ptr_(other.ptr_) {
            // 移动构造函数，只是地址的复制，没有新开内存
            other.ptr_ = nullptr;
            std::cout << "move constructor called: MyClass(MyClass&& other)" << other.ptr_ << std::endl;
        }
        MyClass& operator=(const MyClass& other){
            // 赋值构造函数，也存在开辟内存，复制资源的操作
            if(&other == this){
                return *this;    // 自我赋值，直接返回
            }
            if(ptr_){
                delete ptr_;            //  释放原有内存
            }
            // 逐个赋值
            ptr_ = new int(*other.ptr_);
            return *this;
        }
        ~MyClass(){
            std::cout << "ptr_ = " << ptr_ << std::endl;
            if (ptr_)
            {
                delete ptr_;
            }
            std::cout << "Destructor called." << std::endl;
        }
        int GetValue(void) { return *ptr_; }
        // 打印数据
        void PrintData() const {
            std::cout << "Data: " << *ptr_ << std::endl;
        }
    private:
        int *ptr_;     // 相当于 class 内部管理的资源
};

int main(void){
    // MyClass obj1(10);    // 调用默认构造函数
    // MyClass obj2 = std::move(obj1);    // 调用移动构造函数
    // MyClass obj3(30);     // 使用默认构造函数
    // MyClass obj4(std::move(obj3));      // 调用移动构造函数
    // obj1.PrintData();
    std::vector<MyClass> vec;
    // 不使用移动语义
    MyClass obj5(10);   // 调用默认构造函数
    vec.push_back(obj5);  // 调用复制构造函数
    return 0;
}
