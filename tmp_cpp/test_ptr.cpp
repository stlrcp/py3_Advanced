
/*
// https://blog.csdn.net/FL1768317420/article/details/136385729 二级指针、二级数组、指针数组解析
#include <iostream>
using namespace std;

int main(){
    int p[] = {1, 2, 3, 4};
    int p1[] = {1, 2, 3, 4};
    int p2[] = {1, 2, 3, 4};
    for(int i: p){
        cout << i << endl;
    }
    cout << "p = " << p << endl;
    cout << "p1 = " << p1 << endl;
    cout << "p2 = " << p2 << endl;
    cout << "&p = " << &p << endl;
    int a = 100;
    int *p_a = &a;
    int **p_1 = &p_a;
    int b = 200;
    cout << "&p_a = " << &p_a << " p_a = " << p_a << " *p_a " << *p_a << endl;
    // p_a = &b;
    cout << " a = " << a << endl;
    **p_1 = 300;
    cout << "&a = " << &a << " &b = " << &b << endl;
    cout << "&p_a = " << &p_a << " p_a = " << p_a << " *p_a " << *p_a << endl;
    cout << " a = " << a << endl;

    cout << "**p_1 " << *(*p_1) << endl;
    cout << "*p_1 " << *p_1 << endl;
    int **P_list;
    return 0;
}
*/

#include <iostream>

void printArray(int arr[], int size){
    for (int i = 0; i < size; ++i){
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
}

void printPtr(int* arr[], int size){
    // for (int i = 0; i < size; ++i){
    //     std::cout << arr[i] << " ";
    // }
    std::cout << "arr = " << arr << std::endl;
    std::cout << "*arr = " << *arr << std::endl;
    printArray(*arr, size);
    std::cout << std::endl;
}

int main(){
    int myArray[] = {1, 2, 3, 4, 5};
    int **T;
    std::cout << &myArray << std::endl;
    std::cout << *myArray << std::endl;
    int size = sizeof(myArray) / sizeof(myArray[0]);
    printArray(myArray, size);
    int twoArray[] = {1, 2, 2, 3};
    std::cout << "twoArray = " << twoArray << std::endl;
    int *pA = twoArray;
    std::cout << " pA = " << pA << std::endl;
    std::cout << " &pA = " << &pA << std::endl;
    T = &pA;
    printPtr(T, 4);
    return 0;
}
