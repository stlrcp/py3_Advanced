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
