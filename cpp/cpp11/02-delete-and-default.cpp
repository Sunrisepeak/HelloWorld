/*
clang++ -std=c++11  02-delete-and-default.cpp
g++ -std=c++11  02-delete-and-default.cpp
*/

// C++11 标准 语言特性2 成员函数的 delete 和 default 关键字

#include <iostream>

// 使用 成员函数的 delete 和 default 关键字 的 显示声明
// 去控制编译器对 类型默认成员函数 的生成行为
// 从而去控制 类对象 行为

class A {
public:
    //A(int) { }
    //A() = default;
};

class B {
public:
    //void* operator new(size_t) = delete;
    //void* operator new[](size_t) = delete;

    void operator delete(void*) { };
};

// 对象 不能被 复制
class C {
public:
    C() = default;
    //C(const C &obj) = delete;
    //C & operator=(const C &obj) = delete;
};

int main() {
    {
        A a;
        //A a1(1);
        B b;
        //C c;
    }

    {
        auto aPtr = new A();
        auto bPtr = new B();
        //auto cPtr = new C();
    }

    {
        C c1, c2;
        //C c3(c1);
        //c1 = c2;
    }

}