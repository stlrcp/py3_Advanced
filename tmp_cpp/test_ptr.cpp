
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


/*
#include <iostream>
#include <string>
#include <memory>
using namespace std;
// 动态分配内存，没有释放就 return
void memoryLeak1(){
	string *str = new string("动态分配内存！");
	return;
}
// 动态分配内存，虽然有些释放内存的代码，但是被半路截胡return了
int memoryLeak2(){
	string *str = new string("内存泄漏！");
	// ...
	// 发生某些异常，需要结束函数
	if(1){
		return -1;
	}
	// 另外，使用 try、catch结束函数，也会造成内存泄漏！
	delete str;   // 虽然写了释放内存的代码，但是遭到函数中段返回，使得指针没有得到释放
	return 1;
}
int main(void){
	memoryLeak1();
	memoryLeak2();
	return 0;
}


#include <iostream>
#include <memory>
using namespace std;
class Test{
	public:
		Test() {
			cout << "Test的构造函数..." << endl;
		}
		~Test(){
			cout << "Test的析构函数..." << endl;
		}
		int getDebug() { return this->debug; }
	private:
		int debug = 20;
};
int main(void){
	// Test *test = new Test;   // 只会调用构造函数
	// // delete test;   // 才会调用析构函数  == 
	// auto_ptr<Test> test(new Test);   // 自动调用了析构函数
	// cout << "test->debug: " << test->getDebug() << endl;
	// cout << "(*test).debug: " << (*test).getDebug() << endl;
	// 1. get() 获取智能指针托管的指针地址
	// // 定义智能指针 
	// auto_ptr<Test> test(new Test);
	// Test *tmp = test.get();     // 获取指针返回
	// cout << "tmp->debug: " << tmp->getDebug() << endl;
	// 2. release() 取消智能指针对动态内存的托管
	// auto_ptr<Test> test(new Test);
	// Test *tmp2 = test.release();    // 取消智能指针对内存的托管
	// delete tmp2;   // 之前分配的内存需要自己手动释放
	// 3. reset() 重置智能指针托管的内存地址，，如果地址不一致，原来的会被析构掉
	auto_ptr<Test> test(new Test);
	// test.reset();     // 释放掉智能指针托管的指针内存，并将其置NULL
	test.reset(new Test());   // 释放掉智能指针托管的指针内存，并将参数指针取代之
	cout << "test->debug: " << test->getDebug() << endl;

	return 0;
}


#include <iostream>
#include <string>
#include <memory>
#include <vector>
using namespace std;
class Test{
	public:
		Test() { cout << "Test 的构造函数..." << endl; }
		~Test() { cout << "Test 的析构函数..." << endl; }
		int getDebug() { return this->debug; }
	private:
		int debug = 20;
};
// 不要定义为全局变量，没有意义
// auto_ptr<Test> test(new Test);
void memoryLeak1(){
	// Test *test = new Test;
	// 定义智能指针
	auto_ptr<Test> test(new Test);
	cout << "test->debug: " << test->getDebug() << endl;
	cout << "(*test).debug: " << (*test).getDebug() << endl;
	// get方法
	Test *tmp = test.get();   // 获取指针返回
	cout << "tmp->debug: " << tmp->getDebug() << endl;
	// release 方法
	Test *tmp2 = test.release();   // 取消智能指针对动态内存的托管
	delete tmp2;   // 之前分配的内存需要自己手动释放
	// cout << "======= after the delete tmp2 ====" << endl;
	// reset 方法：重置智能指针托管的内存地址，如果地址不一致，原来的会被析构掉
	test.reset();    // 释放掉智能指针托管的指针内存，并将其置NULL
	// cout << "======= after the test.reset() ====" << endl;
	test.reset(new Test());   // 释放掉智能指针托管的指针内存，并将参数指针取代之
	// 忠告：不要将智能指针定义为指针
	// auto_ptr<Test> *tp = new auto_ptr<Test>(new Test);
	// // 忠告：不要定义指向智能指针对象的指针变量
	// auto_ptr<Test> t1(new Test);
	// auto_ptr<Test> t2(new Test);
	// t1 = t2;
	return;
}
int memoryLeak2(){
	// Test *test = new Test();
	// 定义智能指针
	auto_ptr<Test> test(new Test);
	// ...此处省略一万行代码
	// 发生某些异常，需要结束函数
	if(1){
		return -1;
	}
	// delete test;
	return 1;
}
int main(){
	// memoryLeak1();
	// memoryLeak2();
	// Test *test1 = new Test;
	// auto_ptr<Test> test(new Test);
	// cout << "test->debug: " << test->getDebug() << endl;
	// cout << "(*test).debug: " << (*test).getDebug() << endl;
	// // auto_ptr 被 c++11 抛弃的主要原因
	// auto_ptr<string> p1(new string("I'm Li Ming!"));
	// auto_ptr<string> p2(new string("I'm age 22."));
	// cout << "p1: " << p1.get() << endl;
	// cout << "p2: " << p2.get() << endl;
	// p1 = p2;
	// cout << "p1 = p2 赋值后：" << endl;
	// cout << "p1 : " << p1.get() << endl;
	// cout << "p2 : " << p2.get() << endl;
	// // 弊端2，在STL容器中使用 auto_ptr 存在着重大风险，因为容器内的元素必须支持可复制
	// vector<auto_ptr<string>> vec;
	// auto_ptr<string> p3(new string("I'm P3"));
	// auto_ptr<string> p4(new string("I'm p4"));
	// vec.push_back(std::move(p3));
	// vec.push_back(std::move(p4));
	// cout << "*vec.at(0): " << *vec.at(0) << endl;
	// cout << "vec[1]: " << *vec[1] << endl;
	// // 风险来了
	// vec[0] = vec[1];
	// cout << "vec.at(0): " << *vec.at(0) << endl;
	// cout << "vec[1]: " << *vec[1] << endl;
	// // 弊端3. 不支持对象数组的内存管理
	// auto_ptr<int[]> array(new int[5]);   // 不能这样定义
	return 0;
}


#include <iostream>
#include <memory>
#include <vector>
using namespace std;
int main(){
	// unique_ptr<string> p1(new string("I'm Li Ming!"));
	// unique_ptr<string> p2(new string("I'm age 22."));
	// cout << "p1: " << p1.get() << endl;
	// cout << "p2: " << p2.get() << endl;
	// // p1 = p2;     // 禁止左值赋值
	// // unique_ptr<string> p3(p2);   // 禁止左值赋值构造
	// unique_ptr<string> p3(std::move(p1));
	// p1 = std::move(p2);   // 使用 move 把左值转成右值就可以赋值了，效果和auto_ptr赋值一样
	// cout << "p1 = p2 赋值后：" << endl;
	// cout << "p1: " << p1.get() << endl;
	// cout << "p2: " << p2.get() << endl;
	// cout << "p3: " << p3.get() << endl;
	// // 在 STL 容器中使用 unique_ptr, 不允许直接赋值
	// vector<unique_ptr<string>> vec;
	// unique_ptr<string> p3(new string("I'm P3"));
	// unique_ptr<string> p4(new string("I'm p4"));
	// vec.push_back(std::move(p3));
	// vec.push_back(std::move(p4));
	// cout << "vec.at(0): " << *vec.at(0) << endl;
	// cout << "vec[1]: " << *vec[1] << endl;
	// // vec[0] = vec[1];   // 不允许直接赋值
	// vec[0] = std::move(vec[1]);   // 需要使用move修饰，使得程序员知道后果
	// cout << "vec.at(0): " << *vec.at(0) << endl;
	// cout << "vec[1]: " << *vec[1] << endl;
	// // 支持对象数组的内存管理
	// // 会自动调用 delete[] 函数去释放内存
	// unique_ptr<int[]> array(new int[5]);   // 支持这样定义
	// cout << "array = " << array.get() << endl;
	// cout << "array = " << array[0] << endl;
	return 0;
}


#include <iostream>
#include <memory>
#include <vector>
using namespace std;
class Test{
	public:
		Test() { cout << "Test的构造函数..." << endl; }
		~Test() { cout << "Test的析构函数..." << endl; }
		void doSomething() { cout << "do something......." << endl; }
};
// 自定义一个内存释放
class DestrucTest{
	public:
		void operator()(Test *pt){
			pt->doSomething();
			delete pt;
		}
};
int main(){
	// // 1. 构造
	// // unique_ptr<T> up; 空的unique_ptr, 可以指向类型为T的对象
	// unique_ptr<Test> t1;
	// // unique_ptr<T> up1(new T());   定义 unique_ptr, 同时指向类型为T的对象
	// unique_ptr<Test> t2(new Test);
	// // unique_ptr<T[]> up; 空的 unique_ptr, 可以指向类型为 T[] 的数组对象
	// unique_ptr<int[]> t3;
	// // unique_ptr<T[]> up1(new T[]);   定义 unique_ptr, 同时指向类型为T的数组对象
	// unique_ptr<int[]> t4(new int[5]);
	// // unique_ptr<T, D> up();   空的unique_ptr, 接受一个D类型的删除器D，使得D释放内存
	// unique_ptr<Test, DestrucTest> t5;
	// // unique_ptr<T, D> up(new T()); 定义unique_ptr, 同时指向类型为T的对象，接受一个D类型的删除器D，使得删除器D来释放内存
	// unique_ptr<Test, DestrucTest> t6(new Test);
	// // 2. 赋值
	// unique_ptr<Test> t7(new Test);
	// unique_ptr<Test> t8(new Test);
	// t7 = std::move(t8);    // 必须使用移动语义，结果，t7 的内存释放，t8 的内存交给 t7 管理
	// t7->doSomething();
	// // 3. 主动释放对象
	// unique_ptr<Test> t9(new Test);
	// // t9 = NULL;
	// // t9 = nullptr;
	// // t9.reset();
	// cout << "after t9 = NULL " << endl;
	// // 4. 放弃对象的控制权
	// Test *t10 = t9.release();
	// 5. 重置
	// t9.reset(new Test);
	// 内存管理陷阱
	auto_ptr<string> p1;
	string *str = new string("智能指针的内存管理陷阱");
	p1.reset(str);   // p1 托管 str 指针
	cout << "str: " << *p1 << endl;
	{
		auto_ptr<string> p2;
		p2.reset(str);   // p2 接管str指针时，会先取消 p1的托管，然后再对 str 的托管
	}
	// 此时 p1 已经没有托管内容指针了，为 NULL，再使用它就会内存报错
	cout << "str: " << *p1 << endl;
	// 这是由于 auto_ptr 和 unique_ptr 的排它性所导致的！
	return 0;
}


#include <iostream>
#include <memory>
#include <vector>
using namespace std;
class Person{
	public:
		Person(int v){
			this->no = v;
			cout << "构造函数 \t no = " << this->no << endl;
		}
		~Person(){
			cout << "析构函数 \t no = " << this->no << endl;
		}
	private:
		int no;
};
// 仿函数，内存删除
class DestructPerson{
	public:
		void operator() (Person *pt){
			cout << "DestructPerson..." << endl;
			delete pt;
		}
};
int main(){
	// // 1. 引用计数的使用
	// shared_ptr<Person> sp1;
	// shared_ptr<Person> sp2(new Person(2));
	// // 获取智能指针管控的共享指针的数量  use_count()：引用计数
	// cout << "sp1 use_count() = " << sp1.use_count() << endl;
	// cout << "sp2 use_count() = " << sp2.use_count() << endl;
	// // 共享
	// sp1 = sp2;
	// cout << "sp1 use_count() = " << sp1.use_count() << endl;
	// cout << "sp2 use_count() = " << sp2.use_count() << endl;
	// shared_ptr<Person> sp3(sp1);
	// cout << "sp1 use_count() = " << sp1.use_count() << endl;
	// cout << "sp2 use_count() = " << sp2.use_count() << endl;
	// cout << "sp3 use_count() = " << sp3.use_count() << endl;
	// // 2. 构造
	// shared_ptr<Person> sp1;
	// Person *person1 = new Person(1);
	// sp1.reset(person1);   // 托管 person1
	// shared_ptr<Person> sp2(new Person(2));
	// shared_ptr<Person> sp3(sp1);
	// shared_ptr<Person[]> sp4;
	// shared_ptr<Person[]> sp5(new Person[5]{3, 4, 5, 6, 7});
	// cout << "sp5 use_count() = " << sp5.use_count() << endl;
	// shared_ptr<Person> sp6(NULL, DestructPerson());
	// shared_ptr<Person> sp7(new Person(8), DestructPerson());
	// // 3. 初始化
	// // 方式一： 构造函数
	// shared_ptr<int> up1(new int(10));    // int(10) 的引用计数为1
	// shared_ptr<int> up2(up1);    // 使用智能指针 up1 构造 up2， 此时 int(10) 引用计数为2
	// // 方式二：使用 make_shared 初始化对象，分配内存效率更高（推荐使用）
	// shared_ptr<int> up3 = make_shared<int>(2);   // 多个参数以逗号隔开，最多接受十个
	// shared_ptr<string> up4 = make_shared<string>("字符串");
	// shared_ptr<Person> up5 = make_shared<Person>(9);
	// // 4. 赋值
	// shared_ptr<int> up1(new int(10));
	// shared_ptr<int> up2(new int(11));
	// up1 = up2;   // int(10) 的引用计数减1，计数归零内存释放，up2共享int(11)给up1，int(11)的引用计数为2
	// // 5. 主动释放对象
	// shared_ptr<int> up1(new int(10));
	// up1 = nullptr;   // int(10) 的引用计数减1，计数归零内存释放
	// // 或
	// up1 = NULL;   // 作用同上
	// // 6. 重置
	// shared_ptr<Person> p = make_shared<Person>(10);
	// // shared_ptr<Person> p1 = make_shared<Person>(11);
	// Person *p1 = new Person(1);
	// // p.reset();  // 将p重置为空指针，所管理对象引用计数减1
	// // p.reset(p1); // 将 p 重置为 p1 （的值）, p 管控的对象计数减1，p接管对p1指针的管控
	// p.reset(p1, DestructPerson());   // 将 p 重置为 p1 (的值)，p 管控的对象计数减1并使用 DestructPerson() 作为删除器
	// 7. 交换
	shared_ptr<Person> p1 = make_shared<Person>(10);
	shared_ptr<Person> p2 = make_shared<Person>(11);
	std::swap(p1, p2);   // 交换 p1 和 p2 管理的对象，原对象的引用计数不变
	p1.swap(p2);  // 交换 p1 和 p2 管理的对象，原对象的引用计数不变
	return 0;
}


#include <iostream>
#include <string>
#include <memory>
using namespace std;
class Girl;
class Boy{
	public:
		Boy() {
			cout << "Boy 构造函数" << endl;
		}
		~Boy() {
			cout << "~Boy 析构函数" << endl;
		}
		void setGirlFriend(shared_ptr<Girl> _girlFriend){
			this->girlFriend = _girlFriend;
		}
	private:
		shared_ptr<Girl> girlFriend;
};
class Girl{
	public:
		Girl() {
			cout << "Girl 构造函数" << endl;
		}
		~Girl() {
			cout << "~Girl 析构函数" << endl;
		}
		void setBoyFriend(shared_ptr<Boy> _boyFriend){
			this->boyFriend = _boyFriend;
		}
	private:
		shared_ptr<Boy> boyFriend;
};
void useTrap(){
	shared_ptr<Boy> spBoy(new Boy());
	shared_ptr<Girl> spGirl(new Girl());
	// 陷阱用法
	// spBoy->setGirlFriend(spGirl);
	spGirl->setBoyFriend(spBoy);
	// 此时boy 和 girl 的引用计数都是2
}
int main(){
	useTrap();
	system("pause");
	return 0;
}  // shared_ptr 作为被管控的对象的成员，因循环引用造成无法释放资源
// 在使用 shared_ptr 智能指针时，要注意避免对象交叉使用智能指针的情况！否则会导致内存泄漏
// 解决办法就是使用 weak_ptr 弱指针。


#include <iostream>
#include <string>
#include <memory>
using namespace std;
class Girl;
class Boy{
	public:
		Boy(){
			cout << "Boy 构造函数" << endl;
		}
		~Boy() { cout << "~Boy 析构函数" << endl; }
		void setGirlFriend(shared_ptr<Girl> _girlFriend){
			this->girlFriend = _girlFriend;
		}
	private:
		shared_ptr<Girl> girlFriend;
};
class Girl {
	public:
		Girl() { cout << "Girl 构造函数 " << endl; }
		~Girl() { cout << "~Girl 析构函数 " << endl; }
		void setBoyFriend(shared_ptr<Boy> _boyFriend){
			this->boyFriend = _boyFriend;
		}
	private:
		shared_ptr<Boy> boyFriend;
};
int main(){
	shared_ptr<Boy> spBoy(new Boy());
	shared_ptr<Girl> spGirl(new Girl());
	// 弱指针的使用
	weak_ptr<Girl> wpGirl_1;    // 定义空的弱指针
	weak_ptr<Girl> wpGirl_2(spGirl);   // 使用共享指针构造
	wpGirl_1 = spGirl;     // 允许共享指针赋值给弱指针
	cout << "spGirl \t use_count = " << spGirl.use_count() << endl;
	cout << "wpGirl_1 \t use_count = " << wpGirl_1.use_count() << endl;
	// 弱指针不支持 * 和 -> 对指针的访问
	// *wpGirl_1->setBoyFriend(spBoy);
	spGirl->setBoyFriend(spBoy);
	// (*wpGirl_1).setBoyFriend(spBoy);
	// 在必要的时候可以转换成共享指针
	shared_ptr<Girl> sp_girl;
	sp_girl = wpGirl_1.lock();
	cout << "sp_girl \t use_count = " << sp_girl.use_count() << endl;
	// 使用完之后，再将共享指针置 NULL 即可
	sp_girl = NULL;
	return 0;
}


#include <iostream>
#include <string>
#include <memory>
using namespace std;
class Girl;
class Boy{
	public:
		Boy() { cout << "Boy 构造函数" << endl; }
		~Boy() { cout << "~Boy 析构函数" << endl; }
		void setGirlFriend(shared_ptr<Girl> _girlFriend){
			this->girlFriend = _girlFriend;
			// 在必要的使用可以转换成共享指针
			shared_ptr<Girl> sp_girl;
			sp_girl = this->girlFriend.lock();
			cout << "sp_girl \t use_count = " << sp_girl.use_count() << endl;
			// 使用完之后，再将共享指针置 NULL 即可
			sp_girl = NULL;
		}
	private:
		weak_ptr<Girl> girlFriend;
};
class Girl{
	public:
		Girl() { cout << "Girl 构造函数" << endl; }
		~Girl() { cout << "~Girl 析构函数" << endl; }
		void setBoyFriend(shared_ptr<Boy> _boyFriend){
			this->boyFriend = _boyFriend;
		}
	private:
		shared_ptr<Boy> boyFriend;
};
void useTrap(){
	shared_ptr<Boy> spBoy(new Boy());
	shared_ptr<Girl> spGirl(new Girl());
	spBoy->setGirlFriend(spGirl);
	spGirl->setBoyFriend(spBoy);
}
int main(void) {
	useTrap();
	system("pause");
	return 0;
}   // 在类中使用弱指针接管共享指针，在需要使用时就转换成共享指针去使用即可。


#include <iostream>
#include <memory>
std::weak_ptr<int> gw;
void f(){
	// expired: 判断当前智能指针是否还有托管的对象，有则返回false，无则返回true
	if(!gw.expired()){
		std::cout << "gw is valid\n";   // 有效的，还有托管的指针
	} else{
		std::cout << "gw is expired\n";   // 过期的，没有托管的指针
	}
}
int main(){
	{auto sp = std::make_shared<int>(42);
	gw = sp;
	f();}
	// 当 { } 体中的指针生命周期结束后，再来判断其是否还有托管的指针
	f();
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
