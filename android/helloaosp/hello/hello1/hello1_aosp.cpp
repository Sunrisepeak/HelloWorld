#include <iostream>

#include <dlfcn.h>

#include "helloaosp_api.h" // lib api

#ifdef __LP64__
#define LIB_PATH  "/vendor/lib64/libhelloaosp.v1.so"
#else
#define LIB_PATH  "/vendor/lib/libhelloaosp.v1.so"
#endif

static void *__gLibhandler = nullptr;
static add_type myAdd = nullptr;

void deinitLib() {
    myAdd = nullptr;
    if (__gLibhandler) {
        dlclose(__gLibhandler);
    }
    __gLibhandler = nullptr;
}

bool initLib() {
    
    __gLibhandler = dlopen(LIB_PATH, RTLD_NOW);
    if (nullptr == __gLibhandler) {
        return false;
    }

    auto func_ptr = dlsym(__gLibhandler, "add");

    std::cout << "func_ptr: " << func_ptr << std::endl;

    if (nullptr == func_ptr) {
        deinitLib();
        return false;
    }

    myAdd = reinterpret_cast<add_type>(func_ptr);

    std::cout << "init done" << std::endl;

    return true;
}

int main() {

    if (!initLib()) {
        std::cout << "init failed: " << dlerror() << std::endl;
        return -1;
    }

    int a = 1, b = 2;
    
    std::cout << "Hello AOSP: ";
    std::cout << myAdd(a, b) << std::endl;

    deinitLib();

    return 0;
}