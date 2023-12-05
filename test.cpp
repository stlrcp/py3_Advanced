/*
#include <iostream>
using namespace std;
int main()
{
    cout << "Hello, world!" << endl;
    system("pause");
    return 0;
}
*/

/*
#include <iostream>
using namespace std;
int main()
{
    cout << "Hello, world!" << "\n";
    return 0;
}

#include <iostream>
using namespace std;
int main()
{
    int var1;
    char var2[10];
    cout << "var1 变量的地址：";
    cout << &var1 << endl;
    cout << "var2 变量的地址：";
    cout << &var2 << endl;
    return 0;
}
*/

/*
// myfirst.cpp
#include <iostream>             // a preprocessor directive
int main()                      // function header
{                               // start of function body
    using namespace std;        // make definitions visible
    cout << "Come up and C++ me some time.";        // message
    cout << endl;                   // start a new line
    cout << "You won't regret it!" << endl;     // more  output
    return 0;                       // terminate main()
}                               // end of function body

// carrots.cpp
#include <iostream>
int main()
{
    using namespace std;
    int carrots;            // declare an integer variable
    carrots = 25;           // assign a value to the variable
    cout << "I have ";
    cout << carrots;        // display the value of the variable
    cout << " carrots";
    cout << endl;
    carrots = carrots - 1;      // modify the variable
    cout << "Crunch, crunch, Now I have " << carrots << " carrots." << endl;
    return 0;
}

// getinfo.cpp
#include <iostream>
int main()
{
    using namespace std;
    int carrots;
    cout << "How many carrots do we have?" << endl;
    cin >> carrots;                     // C++ input
    cout << "Here are two more. ";
    carrots = carrots + 2;      // the next line concatenates output
    cout << "Now you have " << carrots << " carrots." << endl;
    return 0;
}

// sqrt.cpp
#include <iostream>
#include <cmath>  // or math.h
int main()
{
    using namespace std;
    double area;
    cout << "Enter the floor area, in square feet, of your home: ";
    cin >> area;
    double side;
    side = sqrt(area);
    cout << "That's the equivalent of a square " << side
    << " feet to the side." << endl;
    cout << "How fascinating! " << endl;
    return 0;
}

// ourfunc.cpp 
#include <iostream>
void simon(int);  // function prototypr for simon()
int main()
{
    using namespace std;
    simon(3);   // call the simon() function
    cout << "Pick an integer: ";
    int count;
    cin >> count;
    simon(count);  // call it again
    cout << "Done!" << endl;
    return 0;
}
void simon(int n)   // define the simon() function
{
    using namespace std;
    cout << "Simon says touch your toes " << n << " times." << endl;
    // void functions don't need return statements
}


//   C++指针与引用实例  https://blog.csdn.net/dgpikaqiu/article/details/120296850   
#include <iostream>
using namespace std;
int main()
{
    int a[10];
    int *p = a;
    int i = 0;
    cout << "请输入10个整数: " << endl;
    for (i=0; i< 10; i++)
    {
        cin >> *(p+i);
    }
    cout << "反转前：" << endl;
    for (i=0; i<10; i++)
    {
        cout << *(p+i) << " ";
    }
    cout << endl;
    p = a;     // 确保指针p指向数组a的首地址
    int* q = p + ((sizeof(a) / sizeof(a[0])) - 1);   // 指针指向数组a的最后一位地址
    while (p < q)
    {
        int t = *p;
        *p = *q;
        *q = t;
        p++;
        q--;
    }
    p = a;      // 确保指针p指向数组a的首地址
    cout << "交换后：" << endl;
    for (i=0; i<10; i++)
    {
        cout << *(p+i) << " ";
    }
    cout << endl;
    return 0;
}


#include <iostream>
using namespace std;
void change(int *a, int *b);
int main()
{
    int x = 2;
    int y = 3;
    cout << "交换前：" << "x= " << x << " " << "y= " << y << endl;
    change(&x, &y);
    cout << "交换后：" << "x= " << x << " " << "y= " << y << endl;
    return 0;
}
void change(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}


// C++ 多线程
// 多线程是多任务处理的一种特殊形式，多任务处理允许让电脑同时运行两个或两个以上的程序。
// 一般情况下，两种类型的多任务处理：基于进程和基于线程。
// - 基于进程的多任务处理是程序的并发执行。
// - 基于线程的多任务处理是同一程序的片段的并发执行。
// 多线程程序包含可以同时运行的两个或多个部分。这样的程序中的每个部分称为一个线程，每个线程定义了一个单独的执行路径。
// 创建线程
// #include <pthread.h>
// pthread_create(thread, attr, start_routine, arg)
// 在这里，pthread_create 创建一个新的线程，并让它可执行。下面是关于参数的说明：
//  thread  ： 指向线程标识符指针。
//  attr    ： 一个不透明的属性对象，可以被用来设置线程属性。您可以指定线程属性对象，也可以使用默认值 NULL。
//  start_routine  :  线程运行函数起始地址，一旦线程被创建就会执行。
//  arg  ： 运行函数的参数，它必须通过把引用作为指针强制转换为 void 类型进行传递，如果没有传递参数，则使用 NULL。
// 创建线程成功时，函数返回 0， 若返回值不为0，则说明创建线程失败。
// 终止线程 ：
// #include <pthread.h>
// pthread_exit(status);
// 在这里，pthread_exit 用于显式地退出一个线程。通常情况下，pthread_exit() 函数是在线程完成工作后无需继续存在时被调用。
// 如果 main() 是在它所创建的线程之前结束，并通过 pthread_exit() 退出，那么其他线程将继续执行。否则，他们将在 main() 结束时自动被终止。
#include <iostream>
#include <pthread.h>   // 必须的头文件
using namespace std;
#define NUM_THREADS 5
// 线程的运行函数
void* say_hello(void* args){
    cout << "Hello Runoob! " << endl;
    return 0;
}
int main(){
    // 定义线程的 id 变量，多个变量使用数组
    pthread_t tids[NUM_THREADS];
    for (int i = 0; i < NUM_THREADS; ++i){
        // 参数依次是：创建的线程 id，线程参数，调用的函数，传入的函数参数
        int ret = pthread_create(&tids[i], NULL, say_hello, NULL);
        if (ret != 0){
            cout << "pthread_create error: error_code= " << ret << endl;
        }
    }
    // 等各个线程退出后，进程才结束，否则进程强制了，线程可能还没反应过来；
    pthread_exit(NULL);
}
*/


//  C++矩阵乘  https://blog.csdn.net/whl0071/article/details/128247620
#include <iostream>
using namespace std;
// Matrix 矩阵乘
class Matrix
{
    public:
        Matrix(int mm, int nn) // 构造函数
        {
            m = mm;
            n = nn;
            int i, j;
            data = new double*[mm];
            for (i=0; i<mm; i++)
                data[i] = new double[nn];
            for (i=0; i<m; i++)  // 矩阵全部元素清零
                for(j=0; j<n; j++)
                    data[i][j] = 0.0;
        }   // 构造M行N列的矩阵

        Matrix(const Matrix &src)    // 拷贝构造函数
        {
            m = src.m;
            n = src.n;
            int i, j;
            data = new double*[m];  // 动态建立二维数组
            for(i=0; i<m; i++)
                data[i] = new double[n];
            for(i=0; i<m; i++)   // 动态数组赋值
                for(j=0; j<n; j++)
                    data[i][j] = src.data[i][j];
        }

        ~Matrix()  // 析构函数
        {
            for(int i=0; i<m; i++)
                delete []data[i];
            delete []data;
        }
        Matrix& operator=(const Matrix &src);   // 重载"="运算符
        Matrix operator * (const Matrix &m2);   // 矩阵乘法
        void display();
        void input();
        private:
            double **data;
        int m, n;   // 矩阵的行数，列数
};  // 类定义结束

Matrix& Matrix::operator=(const Matrix &src)   // 重载"="运算符
{
    int i,j;
    for (i=0; i<m; i++)
        delete []data[i];
    delete []data;
    m=src.m; n=src.n;
    data = new double*[m];   // 动态建立二维数组
    for (i=0; i<m; i++)
        data[i] = new double[n];
    for (i=0; i<m; i++)
        for (j=0; j<n; j++)
            data[i][j] = src.data[i][j];
    return *this;
}
// 矩阵* 运算符重载
Matrix Matrix::operator *(const Matrix &m2)   // 矩阵乘法的实现
{
    Matrix m3(this->m, m2.n);
    if (this->n != m2.m)
    {
        cout << "两矩阵无法进行乘法运算. \n" << endl;
        exit(0);
    }
    int i,j,k,l;
    for (i=0; i<this->m; i++)
        for (j=0; j<m2.n; j++)
        {
            for (k=0; k<this->n; k++)
            {
                m3.data[i][j] += this->data[i][k]*m2.data[k][j];
            }
        }
    return m3;
}
// 输入矩阵元素
void Matrix::input()
{
    for (int i=0; i<m; i++)
        for (int j=0; j<n; j++)
            cin >> data[i][j];
}
// 显示矩阵元素
void Matrix::display()
{
    int i,j;
    for (i=0; i<m; i++)
    {
        for (j=0; j<n; j++)
        {
            cout << data[i][j] << " ";
        }
        cout << endl;
    }
}
// 主函数
int main(int argc, char* argv[])
{
    int x,y;
    cout << "矩阵1行数: ";
    cin >> x;
    cout << "矩阵1列数: ";
    cin >> y;
    Matrix A(x, y);
    cout << "请输入矩阵1元素  (按行，共" << x*y << " 个)" << endl;
    A.input();
    cout << "矩阵1: " << endl;
    A.display();
    cout << "矩阵2行数: ";
    cin >> x;
    cout << "矩阵2列数: ";
    cin >> y;
    Matrix B(x, y);
    cout << "请输入矩阵2元素 (按行，共" << x*y << " 个)" << endl;
    B.input();
    cout << "矩阵2: " << endl;
    B.display();
    Matrix C=A*B;
    cout << "矩阵1 与 矩阵2 的乘积: " << endl;
    C.display();
    return 0;
}
