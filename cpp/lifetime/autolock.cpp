#include <iostream>
#include <string>
#include <mutex>
#include <thread>
#include <chrono>

/*

g++ cpp/lifetime/autolock.cpp && ./a.out

*/

struct AutoLog {
    AutoLog(std::string name) {
        mFuncName = name;
        std::cout << mFuncName << " start" << std::endl; }
    ~AutoLog() { std::cout << mFuncName << " end" << std::endl; }
    std::string mFuncName;
};

struct AutoLock {
    AutoLock(std::mutex *mPtr) : mMutexPtr { mPtr } {
        mMutexPtr->lock();
    }
    ~AutoLock() { mMutexPtr->unlock(); }
    std::mutex *mMutexPtr;

    AutoLock(const AutoLock &) = delete;
    AutoLock & operator=(const AutoLock &) = delete;
};

static int n = 0;
std::mutex m;
void add(int threadId) {
    //m.lock();
    //AutoLog _alog(std::to_string(threadId) + "-add");
    //...
    {
        AutoLock _al(&m);
        n++;
    }
    //...
    std::cout << "n is " << n << std::endl;
    //m.unlock();
}

#define N 50000

// 生命周期机制-妙用2 - AutoLock - 作用域锁

int main() {
    AutoLog _alog("main");

    std::thread t0([]{ for (int i = 0; i < N; i++) add(0); });
    std::thread t1([]{ for (int i = 0; i < N; i++) add(1); });

    std::this_thread::sleep_for(std::chrono::seconds(1));

    if (t0.joinable()) t0.join(); if (t1.joinable()) t1.join();
    if (n != N * 2) {
        std::cout << "compute error..." << std::endl;
        return -1;
    }
    std::cout << "success: n is " << n << std::endl;
    return 0;
}