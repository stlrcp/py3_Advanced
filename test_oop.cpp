/*
#include <iostream>
#include <ctime>

using namespace std;

int main()
{
    time_t now = time(0);
    // cout << now << endl;
    char *dt = ctime(&now);
    cout << "本地日期和时间：" << dt << endl;
}


#include <iostream>
using namespace std;

class Box
{
    public:
        double length;
        double breadth;
        double height;
        // 成员函数声明
        double get(void);
        void set(double len, double bre, double hei);
};

// 成员函数定义
double Box::get(void)
{
        return length * breadth * height;
}

void Box::set(double len, double bre, double hei)
{
        length = len;
        breadth = bre;
        height = hei;
}

int main() {
        Box Box1;
        Box Box2;
        Box Box3;
        double volume = 0.0;   // 用于存储体积

        // box1 详述
        Box1.height = 5.0;
        Box1.length = 6.0;
        Box1.breadth = 7.0;

        // box2 详述
        Box2.height = 10.0;
        Box2.length = 12.0;
        Box2.breadth = 13.0;

        // box1 的 体积
        volume = Box1.height * Box1.length * Box1.breadth;
        cout << "Box1 的体积： " << volume << endl;

        // box2 的体积
        volume = Box2.height * Box2.length * Box2.breadth;
        cout << "Box2 的体积： " << volume << endl;

        // box3 详述
        Box3.set(16.0, 8.0, 12.0);
        volume = Box3.get();
        cout << "Box3 的体积：" << volume << endl;
        return 0;
}



#include <iostream>
using namespace std;

class a
{
    long a0;
    public:
        a(long b) {
            a0 = b;
        }
        void geta(){
            cout << a0 << endl;
        }
};
int main() {
        a b(5);  // 定义对象b, 并给 b 中的 a0 赋初值
        long *p;
        p = (long *)&b;  // 令指针 p 指向 b 中前 4 个字节，在这里相当于指向 a0
        b.geta();       // 用内部函数访问 a0
        cout << *p << endl;   // 在外部直接访问 a0
        *p = 8;    // 在外部改变 a0 的值
        b.geta();   // 输出改变后的结果
        cout << *p << endl;
        return 0;
}   //  需要注意的是，使用这种方法虽然可以用于基于类的多态原则的一些程序开发，但违反了类的封装原则，在使用指针的类中也极不安全，所以不建议使用


// 类对象初始化的时候加括号与不加括号有什么区别
#include <iostream>
using namespace std;
class A
{
    public:
        A(){
            cout << "A()" << endl;
        }
        A(int a)
        {
            cout << "A(int a)" << endl;
        }
};

int main()
{
        // 栈上
        A a();   // 这里声明了一个函数，没有传入的参数，返回值为类类型
        cout << "~~~~~~~~~~~~~~" << endl;
        A b;  // 默认调用 "对象名（）" 这个构造函数构造对象
        cout << "~~~~~~~~~~~~~~~" << endl;
        A c(1);   // 默认调用相应的构造函数构造对象

        // 堆上，加括号不加括号无差别，都调用默认的构造函数
        A *d = new A();
        A *e = new A;

        // 对于内置类型而言，加括号是进行了初始化，不加是未进行初始化
        int *f = new int();
        int *g = new int;

        cout << *f << endl;
        cout << *g << endl;
        return 0;
}



#include <iostream>
using namespace std;

class Box
{
    public:
        double length;    // 长度
        double breadth;    // 宽度
        double height;   // 高度
        // 成员函数声明
        double get(void);
        void set(double len, double bre, double hei);
};
// 成员函数定义
double Box::get(void)
{
        return length * breadth * height;
}
void Box::set(double len, double bre, double hei)
{
        length = len;
        breadth = bre;
        height = hei;
}
int main()
{
        Box Box1;    // 声明 Box1，类型为 Box
        Box Box2;   // 声明 Box2, 类型为 Box
        double volume = 0.0;  // 用于存储体积

        // box 1 详述
        Box1.height = 5.0;
        Box1.length = 6.0;
        Box1.breadth = 7.0;

        // box 1 的 体积
        volume = Box1.height * Box1.length * Box1.breadth;
        cout << "Box1 的地址：" << &Box1 << endl;
        cout << "Box1 的体积：" << volume << endl;

        // Box 2
        volume = Box2.get();
        cout << "Box2 的地址：" << &Box2 << endl;
        cout << "Box2 的体积：" << volume << endl;

        Box2 = Box1;   // 这时是把Box1的成员变量值复制给了Box2，Box2还是原来的对象，并没有被销毁，对象地址还是原来的地址。
        volume = Box2.get();
        cout << "Box2 的地址：" << &Box2 << endl;
        cout << "Box2 的体积：" << volume << endl;
}



// 数据封装是面向对象编程的一个重要特点，它防止函数直接访问类类型的内部成员
// 公有（public）成员
#include <iostream>
using namespace std;

class Line
{
    public:
        double length;
        void setLength(double len);
        double getLength(void);
};
// 成员函数定义
double Line::getLength(void)
{
        return length;
}
void Line::setLength(double len)
{
        length = len;
}

// 主函数
int main()
{
        Line line;
        // 设置长度
        line.setLength(6.0);
        cout << "Length of line : " << line.getLength() << endl;
        // 不使用成员函数设置长度
        line.length = 10.0;    // OK, 因为 length 是公有的
        cout << "Length of line : " << line.length << endl;
        return 0;
}


// 私有（private）成员
// 私有成员变量或函数 在类的外部是不可访问的，甚至是不可查看的，只有类和友元函数可以访问私有成员。
// 默认情况下，类的所有成员都是私有的。
#include <iostream>
using namespace std;
class Box
{
    public:
        double length;
        void setWidth(double wid);
        double getWidth(void);
    private:
        double width;
};
// 成员函数定义
double Box::getWidth(void)
{
        return width;
}
void Box::setWidth(double wid)
{
        width = wid;
}
// 程序的主函数
int main()
{
        Box box;
        // 不使用成员函数设置长度
        box.length = 10.0;  // OK, 因为 length 是公有的
        cout << "Length of box : " << box.length << endl;

        // 不使用成员函数设置宽度
        // box.width = 10.0;   // Error, 因为 width 是私有的
        box.setWidth(8.0);    // 使用成员函数设置宽度
        cout << "Width of box : " << box.getWidth() << endl;
        return 0;
}


// protected (受保护) 成员
// protected 成员变量或函数与私有成员十分相似，但有一点不同，protected 成员在派生类（即子类）中是可访问的。
#include <iostream>
using namespace std;

class Box
{
    protected:
        double width;
};

class SmallBox:Box  // SmallBox 是派生类
{
    public:
        void setSmallWidth(double wid);
        double getSmallwidth(void);
};
// 子类的成员函数
double SmallBox::getSmallwidth(void)
{
        return width;
}
void SmallBox::setSmallWidth(double wid)
{
        width = wid;
}
// 程序的主函数
int main()
{
        SmallBox box;
        // 使用成员函数设置宽度
        box.setSmallWidth(5.0);
        cout << "Width of box : " << box.getSmallwidth() << endl;
        return 0;
}



// 继承中的特点
// 有 public、protected、private 三种继承方式，它们相应地改变了基类成员的访问属性
// 1. public 继承：基类 public 成员、protected成员、private 成员的访问属性在派生类中分别变成：public、protected、private
// 2. protected 继承：基类 public 成员、protected 成员、private 成员的访问属性在派生类中分别变成：protected、protected、private
// 3. private 继承： 基类 public 成员，protected 成员，prvate 成员的访问属性在派生类中分别变成：private、private、private
// 但无论哪种继承方式，下面两点都没有改变：
// 1. private 成员只能被本类成员（类内）和友元访问，不能被派生类访问；
// 2. protected 成员可以被派生类访问。
// public继承
#include <iostream>
#include <assert.h>
using namespace std;
class A{
    public:
        int a;
        A(){
            a1 = 1;
            a2 = 2;
            a3 = 3;
            a = 4;
        }
        void fun() {
            cout << a << endl;
            cout << a1 << endl;
            cout << a2 << endl;
            cout << a3 << endl;
        }
    public:
        int a1;
    protected:
        int a2;
    private:
        int a3;
};
class B : public A{
    public:
        int a;
        B(int i){
            A();
            A tmp;
            tmp.fun();
            a = i;
        }
        void fun() {
            cout << a << endl;
            cout << a1 << endl;
            cout << a2 << endl;
            // cout << a3 << endl;    // 错误，基类的private成员不能被派生类访问
        }
};
int main() {
        B b(10);
        cout << b.a << endl;
        cout << b.a1 << endl;
        // cout << b.a2 << endl;   // 错误，类外不能访问 protected 成员
        // cout << b.a3 << endl;   // 错误，类外不能访问 private 成员
        b.fun();
        return 0;
}



// protected 继承
#include <iostream>
#include <assert.h>
using namespace std;
class A{
    public:
        int a;
        A(){
            a1 = 1;
            a2 = 2;
            a3 = 3;
            a = 4;
        }
        void fun(){
            cout << a << endl;
            cout << a1 << endl;
            cout << a2 << endl;
            cout << a3 << endl;
        }
    public:
        int a1;
    protected:
        int a2;
    private:
        int a3;
};
class B : protected A{
    public:
        int a;
        B(int i){
            A();
            A tmp;
            tmp.fun();
            a = i;
        }
        void fun() {
            cout << a << endl;
            cout << a1 << endl;
            cout << a2 << endl;
            // cout << a3 << endl; // 错误，基类的 private 成员不能被派生类访问
        }
};
int main(){
        B b(10);
        cout << b.a << endl;    // 正确，public成员
        // cout << b.a1 << endl;    // 错误，protected 成员不能再类外访问
        // cout << b.a2 << endl;    // 错误，protected 成员不能在类外访问
        // cout << b.a3 << endl;    // 错误，private 成员不能在类外访问
        b.fun();
        return 0;
}
*/


// private 继承
#include <iostream>
#include <assert.h>
using namespace std;
class A
{
public:
    int a;
    A()
    {
        a1 = 1;
        a2 = 2;
        a3 = 3;
        a = 4;
    }
    void fun()
    {
        cout << a << endl;
        cout << a1 << endl;
        cout << a2 << endl;
        cout << a3 << endl;
    }

public:
    int a1;

protected:
    int a2;

private:
    int a3;
};
class B : private A{
    public:
        int a;
        B(int i) {
            A();
            A tmp;
            tmp.fun();
            a = i;
        }
        void fun(){
            cout << a << endl; // 正确， public 成员
            cout << a1 << endl;  // 正确，基类 public 成员，在派生类中变成了 private，可以被派生类访问
            cout << a2 << endl;   // 正确，基类的 protected 成员，在派生类中变成了 private，可以被派生类访问
            // cout << a3 << endl;   // 错误，基类的 private 成员不能被派生类访问
        }
};
int main(){
        B b(10);
        cout << b.a << endl;    // 正确，public成员
        // cout << b.a1 << endl;    // 错误，private 成员不能在类外访问
        // cout << b.a2 << endl;    // 错误，private 成员不能在类外访问
        // cont << b.a3 << endl;    // 错误，private 成员不能再类外访问
        b.fun();
        return 0;
}
