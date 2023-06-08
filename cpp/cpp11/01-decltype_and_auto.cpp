// g++ 01-decltype_and_auto.cpp --std=c++11

#include <vector>
#include <type_traits>
#include <cassert>

// 仅做语法说明, 不建议滥用类型推导把简单事情复杂化
void syntax() {
    int a = 0;
    auto b = a;          // int b = a;
    decltype(b) c = b;   // int c = b;
    decltype(a) *d = &a; // int *d = &a;
    static_assert(std::is_same<decltype(b), int>::value == true);
    static_assert(std::is_same<decltype(c), int>::value == true);
    static_assert(std::is_same<decltype(d), int *>::value == true);
}

// 复杂类型定义: 例如容器迭代器类型
void complex_type() {
    std::vector<int> vec(10, 1);

    for (std::vector<int>::iterator it = vec.begin(); it != vec.end(); it++) {
        ;
    }

    for (auto it = vec.begin(); it != vec.end(); it++) {
        static_assert(std::is_same<decltype(it), std::vector<int>::iterator>::value);
    }

    static_assert(std::is_same<decltype(vec.begin()), std::vector<int>::iterator>::value);

}

// 复杂类型定义: lambda 表达式
void lambda_expr() {
    auto add = [](int a, double b) {
        return a + b;
    };
    decltype(add) add_func = add;
    double c = add_func(1, 2.2);
    assert(c == 3.2);
}

// 表达式类型
void expression() {
    char a = '0';
    int b = 1;
    double c = 2;
    decltype(a + b + c) d = a + b + c; // double d
    auto f = a + b + c;                // double f
    static_assert(std::is_same<decltype(d), double>::value);
    static_assert(std::is_same<decltype(f), double>::value);
}

struct A {
    int data;
};

void decltype_lvalue_expr() {
    A a;

    // 对象a.data
    decltype(a.data) b; // int b;
    static_assert(std::is_same<decltype(b), int>::value);

    // (a.data) 是一个表达式
    decltype((a.data)) c = a.data; // int &c = a.data;
    static_assert(std::is_same<decltype(c), int &>::value);

    const A a1 = a;

    // a1.data = 1; // err
    // 对象a.data
    decltype(a1.data) b1; // int b1;
    static_assert(std::is_same<decltype(b1), int>::value);

    // (a.data) 是一个表达式
    decltype((a1.data)) c1 = a1.data; // const int &c1 = a1.data;
    static_assert(std::is_same<decltype(c1), const int &>::value);

}

void other() {
    {// 差别1：声明不初始化
        decltype(1 + 1.1) a;
        // auto a; // err
    }

    {// 差别2：仅需要类型信息
        A a;
        std::vector<decltype(a)> vec;
        auto intPtr = reinterpret_cast<decltype(a.data) *>(&a);
    }

    {// 不推荐对简单类型使用类型推导
        int a = 1;
        auto b = a;
    }

    {// 此时不推荐decltype
        std::vector<int> vec;
        decltype(vec.begin()) _begin1 = vec.begin(); // 不推荐
        auto begin1 = vec.begin();
    }
}

int main() {
    syntax();
    complex_type();
    lambda_expr();
    expression();
    decltype_lvalue_expr();
    other();
}