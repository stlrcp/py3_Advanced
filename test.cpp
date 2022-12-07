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
*/
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

