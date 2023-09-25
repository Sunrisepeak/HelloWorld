#include <iostream>
#include <cassert>

#include <dstruct.hpp>

/*

g++ dstruct/simple_allocator.cpp -I ../DStruct && ./a.out

*/

//#define DEBUG

#define LOGI(...) printf("%s: ", __func__); printf(__VA_ARGS__); printf("\n")

#ifdef DEBUG
#define LOGD(...) LOGI(__VA_ARGS__)
#else
#define LOGD(...)
#endif

char array[1024] { 0 }; // 1k memory

// mem-flag: 0 free, other allocated
#define MEM_BLOCK_SIZE 32
struct SimpleAllocator {

    // Unused-Flag 0
    using MemBlockFlag = unsigned long long;

    struct MemBlock {
        MemBlockFlag flag; // flag area
        char mem[MEM_BLOCK_SIZE - sizeof(MemBlockFlag)]; // useable area
    };

    static void init() {
        LOGI("init allocate: memory address %p, size %ld", array, sizeof(array));
        char *memPtr = array;
        while (memPtr + sizeof(MemBlock) < array + sizeof(array)) {
            auto mbPtr = (MemBlock *)memPtr;
            mbPtr->flag = 0;
            memPtr = memPtr + MEM_BLOCK_SIZE;
            LOGD("address %p, block-size %ld", mbPtr, sizeof(MemBlock));
        }
    }

    static void * malloc(int size) {

        assert(size <= sizeof(MemBlock) - sizeof(MemBlockFlag));

        bool allocateFailed = true;
        MemBlock *mbPtr = nullptr;

        for (int i = 0; i <= sizeof(array) - sizeof(MemBlock); i += sizeof(MemBlock)) {
            mbPtr = (MemBlock *)(array + i);
            if (mbPtr->flag == 0) {
                allocateFailed = false;
                break;
            }
        }

        if (allocateFailed) {
            LOGI("request size %d, memory allocate failed...", size);
            return nullptr;
        }

        LOGD("addr %p, request size %d", mbPtr, size);

        mbPtr->flag = size;

        return &(mbPtr->mem);
    }

    static void free(void *ptr) {
        auto mbPtr = (MemBlock *)((char *)ptr - sizeof(MemBlockFlag));

        LOGD("addr %p, size %lld, block-size %d", mbPtr, mbPtr->flag, MEM_BLOCK_SIZE);

        assert(
            array <= (char *)mbPtr &&
            (char *)mbPtr <= array + sizeof(array) - sizeof(MemBlock) &&
            "memory free failed - range"
        );

        assert(mbPtr->flag != 0 && "memory free failed - flag error(double free)");

        mbPtr->flag = 0;
    }
};

struct RGB {
    char r;
    short g;
    char b;
};

// test SimpleAllocator
int main() {

    dstruct::Vector<int *> ptrVec;

    SimpleAllocator::init();

    for (int i = 0; i < 50; i++) {
        auto intPtr = (int *) SimpleAllocator::malloc(sizeof(int));

        if (intPtr == nullptr)
            break;

        *intPtr = i;
        ptrVec.push_back(intPtr);
    }

    RGB *rgbPtr = (RGB *) SimpleAllocator::malloc(sizeof(RGB));

    if (rgbPtr == nullptr) {
        int *intPtr = ptrVec.back();
        LOGI("free %d, addr %p", *intPtr, intPtr);
        SimpleAllocator::free(ptrVec.back());
        ptrVec.pop_back();
        rgbPtr = (RGB *) SimpleAllocator::malloc(sizeof(RGB));
    }

    rgbPtr->r = 1;
    rgbPtr->g = 2;
    rgbPtr->b = 3;

    LOGI("rgb: (%d, %d, %d)", rgbPtr->r, rgbPtr->g, rgbPtr->b);

    for (int i = 0; i < ptrVec.size(); i++) {
        SimpleAllocator::free(ptrVec[i]);
    }

// failed test set
    //SimpleAllocator::malloc(25); // size limit
    //SimpleAllocator::free(ptrVec[0]); // test double free

    return 0;
}
