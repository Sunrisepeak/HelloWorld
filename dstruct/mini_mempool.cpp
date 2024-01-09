// https://github.com/Sunrisepeak/HelloWorld/dstruct/mini_mempool.cpp
// https://github.com/Sunrisepeak/DStruct

#include <unistd.h> // system call
#include <iostream>
#include <dstruct.hpp> 

/*

g++ dstruct/mini_mempool.cpp -I libs/DStruct && ./a.out

*/


#define DEBUG

#define LOGI(...) printf("%s: ", __func__); printf(__VA_ARGS__); printf("\n")

#ifdef DEBUG
#define LOGD(...) LOGI(__VA_ARGS__)
#else
#define LOGD(...)
#endif

class MiniMemPool {
    /*
    struct MemBlock {
        dstruct::_SinglyLink linker;
        int size; // or use size_t
    };
    */
    using Linker = dstruct::_SinglyLink;
    using MemBlock = dstruct::_EmbeddedListNode<int, Linker>;
    using MemBlockList = MemBlock;

public:
    static void * allocate(int bytes) {
        void *memPtr = nullptr;
        int alignedSize = _MEM_ALIGN_ROUND_UP(bytes);
        MemBlock *memBlkPtr = _Instance()._memblk_search_ffma(alignedSize);
        LOGD("request bytes %d, align to %d", bytes, alignedSize);

        if (memBlkPtr == nullptr) {
            LOGD("not found mem-block in mempool, and try to request by sbrk");
            memPtr = sbrk(bytes);
            _Instance()._mPoolEndAddr = reinterpret_cast<char *>(memPtr) + bytes;
            LOGD("sbrk %p, update mem-pool end addr to %p", memPtr, _Instance()._mPoolEndAddr);
        } else {
            memPtr = memBlkPtr;
            if (memBlkPtr->data >= alignedSize + sizeof(MemBlock)) {
                auto *memFragmentPtr = reinterpret_cast<char *>(memPtr) + alignedSize;
                MemBlock *memFragmentBlkPtr = reinterpret_cast<MemBlock *>(memFragmentPtr);
                memFragmentBlkPtr->data = memBlkPtr->data - alignedSize;
                _Instance()._memblk_insert(memFragmentBlkPtr);
                LOGD("split mem-block from [%p, %d] to [[%p, %d], [%p, %d]], and insert to mem-pool",
                    memBlkPtr, memBlkPtr->data,
                    memBlkPtr, alignedSize, memFragmentBlkPtr, memFragmentBlkPtr->data
                );
            }
        }

        LOGD("return memory address %p, real size %d", memPtr, alignedSize);

        return memPtr;
    }

    static void deallocate(void *addr, int bytes) {
        // mem_valid_check(addr);
        auto memBlkPtr = reinterpret_cast<MemBlock *>(addr);
        memBlkPtr->data = _MEM_ALIGN_ROUND_UP(bytes);
        LOGD("release memory to mempool: addr %p, size %d(%d)", addr, bytes, memBlkPtr->data);
        _Instance()._memblk_insert(memBlkPtr);
    }

    static int free_mem_size() {
        return _Instance()._mFreeMemSize;
    }

protected:
    //void *_mPoolStartAddr, *_mPoolEndAddr;
    int _mFreeMemSize;
    char *_mPoolStartAddr, *_mPoolEndAddr;
    MemBlock _mFreeMemBlockList;

    MiniMemPool() : _mFreeMemSize { 1024 }, _mPoolStartAddr { nullptr }, _mPoolEndAddr { nullptr } {
        MemBlockList::init(&_mFreeMemBlockList);
        (char *)sbrk(0); // init heap
        _mPoolStartAddr = (char *)sbrk(_mFreeMemSize);
        _mPoolEndAddr = _mPoolStartAddr + _mFreeMemSize;

        assert(_mPoolStartAddr != (void *)ENOMEM);
        LOGI("init: mem-pool start addr %p, mempool end addr %p, free memory size %d",
            _mPoolStartAddr, _mPoolEndAddr, _mFreeMemSize);

        // init list
        auto *memBlkPtr = reinterpret_cast<MemBlock *>(_mPoolStartAddr);
        memBlkPtr->data = 1024;
        MemBlockList::add(&_mFreeMemBlockList, memBlkPtr);
    }

    MiniMemPool(const MiniMemPool &) = delete;
    MiniMemPool &operator=(const MiniMemPool &) = delete;

    ~MiniMemPool() {
        brk(_mPoolStartAddr);
        _mPoolEndAddr = _mPoolEndAddr = nullptr;
        _mFreeMemSize = 0;
        LOGI("release all memory by brk-syscall");
    }

    static MiniMemPool & _Instance() {
        static MiniMemPool miniMemPool; // create & manage static memory area
        return miniMemPool;
    }

    MemBlock * _memblk_search_ffma(int size) {
        Linker *prevLinkPtr = MemBlockList::to_link(&_mFreeMemBlockList);
        MemBlock *memBlkPtr = nullptr;
        while (prevLinkPtr->next != MemBlockList::to_link(&_mFreeMemBlockList)) {
            auto nodePtr = MemBlockList::to_node(prevLinkPtr->next);
            if (nodePtr->data >= size) {
                Linker::del(prevLinkPtr, prevLinkPtr->next /* nodePtr */);
                memBlkPtr = nodePtr;
                break;
            }
            prevLinkPtr = prevLinkPtr->next;
        }
        return memBlkPtr;
    }

    void _memblk_insert(MemBlock *memBlkPtr) {
        MemBlockList::add(&_mFreeMemBlockList, memBlkPtr);
    }

    static int _MEM_ALIGN_ROUND_UP(int bytes) {
        return (((bytes) + sizeof(MemBlock) - 1) & ~(sizeof(MemBlock) - 1));
    }

};

int main() {

    void* memBlockPtrArr[10] { 0 };
    size_t memBlockSize = 40;

    for (int i = 0; i < 10; i++) {
        memBlockPtrArr[i] = static_cast<int *>(malloc(memBlockSize));
        std::cout << "malloc: " << memBlockPtrArr[i] << std::endl;
    }

    for (int i = 0; i < 10; i++) {
        std::cout << "free: " << memBlockPtrArr[i] << std::endl;
        free(memBlockPtrArr[i]);
    }

    printf("\n---------------------------------------------------------\n\n");

    auto memPtr1 = MiniMemPool::allocate(100);
    LOGD("fmemPtr1 %p", memPtr1);
    MiniMemPool::deallocate(memPtr1, 100);
    auto memPtr2 = MiniMemPool::allocate(100);
    LOGD("memPtr2 %p", memPtr2);
    MiniMemPool::deallocate(memPtr2, 100);

    for (int i = 0; i < 10; i++) {
        memBlockPtrArr[i] = static_cast<int *>(MiniMemPool::allocate(memBlockSize));
        std::cout << "MiniMemPool::allocate: " << memBlockPtrArr[i] << std::endl;
    }

    for (int i = 0; i < 10; i++) {
        std::cout << "MiniMemPool::deallocate: " << memBlockPtrArr[i] << std::endl;
        MiniMemPool::deallocate(memBlockPtrArr[i], memBlockSize);
    }   

    auto ptr = MiniMemPool::allocate(1024);
    MiniMemPool::deallocate(ptr, 1024);

    LOGI("MiniMemPool free memory size is %d", MiniMemPool::free_mem_size());

    return 0;
}