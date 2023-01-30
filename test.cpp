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
*/

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








