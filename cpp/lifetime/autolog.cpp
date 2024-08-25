#include <iostream>
#include <string>

/*

g++ cpp/lifetime/autolog.cpp && ./a.out

*/

struct AutoLog {
    AutoLog(std::string name) {
        mFuncName = name;
        std::cout << mFuncName << " start" << std::endl; }
    ~AutoLog() { std::cout << mFuncName << " end" << std::endl; }
    std::string mFuncName;
};

// 生命周期机制-妙用1 - AutoLog - 函数执行开始/结束-log打印

void test(int n) {
    AutoLog _al("test");
    std::cout << "test - start" << std::endl;
    //... test impl
    std::cout << "n is " << n << std::endl;
    if (n == 2) {
        return;
    }
    //...
    std::cout << "test - end" << std::endl;
}

int main() {
    std::cout << "main - start" << std::endl;
    {
        AutoLog _alog("call test");
        test(2);
    }
    std::cout << "main - end" << std::endl;
    return 0;
}