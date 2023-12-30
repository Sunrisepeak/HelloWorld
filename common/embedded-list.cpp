#include <iostream>
#include <cassert>

#include <dstruct.hpp>

// g++ -Ilibs/DStruct common/embedded-list.cpp && ./a.out

// C-Style
struct IntList {
    int data;
    struct IntList *next;
};

void IntList_init(struct IntList *list);
bool IntList_empty(struct IntList *list);
void IntList_add(struct IntList *prev, struct IntList *curr);
void IntList_del(struct IntList *prev, struct IntList *curr);

struct DoubleList {
    double data;
    struct DoubleList *next;
};

void DoubleList_init(struct DoubleList *list);
bool DoubleList_empty(struct DoubleList *list);
void DoubleList_add(struct DoubleList *prev, struct DoubleList *curr);
void DoubleList_del(struct DoubleList *prev, struct DoubleList *curr);


// Embedded

struct Student {
    char *name;
    int age;
};

struct StudentListNode {
    dstruct::_SinglyLink linker; // 链表链接器
    char *name;
    int age;
};

struct _StudentListNode {
    struct _StudentListNode *next; // 链表链接器
    Student student;
};


struct MyList {
    int a;
    dstruct::_SinglyLink linker;
    double b;
    char c;
};

using MyListNode = MyList;

// 成员地址-相对偏移
#define offset_of(StructType, member)	((size_t)&((StructType *)0)->member)

// Linker视角转节点视角: 通过成员地址 获取完整结构体类型
#define to_node(linkPtr, StructType, member) \
	( \
        (StructType *)( (char *)linkPtr - offset_of(StructType, member) ) \
    )
// 节点视角转linker视角:
#define to_link(nodePtr) (&((nodePtr)->linker))

int main() {

// example1: Generic-Style / C-No-Generic-Style
    dstruct::SLinkedList<int> intList1;
    struct IntList intList2;

    dstruct::SLinkedList<double> doubleList1;
    struct IntList doubleList2;

// example2: embedded DS
    dstruct::SLinkedList<Student> studentList1;
    dstruct::_SinglyLink studentList2;

    dstruct::_SinglyLink::init(&studentList2);

    StudentListNode sNode;
    dstruct::_SinglyLink::add(&studentList2, &(sNode.linker));

// example3

    // 创建&初始化链表
    MyList myList;
    dstruct::_SinglyLink::init(to_link(&myList));

    // 初始化node并添加到链表
    for (int i = 0; i < 10; i++) {
        // 分配内存
        MyListNode *node = (MyListNode *) malloc(sizeof(MyListNode));
        // 初始化
        node->a = i;
        node->b = 0.5 + i;
        node->c = 'a' + i;
        // 添加到链表(头插法)
        dstruct::_SinglyLink::add(to_link(&myList), to_link(node));
    }

    assert(!dstruct::_SinglyLink::empty(to_link(&myList)));

    // 遍历节点 访问数据 并释放节点
    auto linkPtr = to_link(&myList)->next; // 获取第一个节点地址
    for (; linkPtr != to_link(&myList); linkPtr = linkPtr->next) {
        auto nodePtr = to_node(linkPtr, MyListNode, linker); // 1.转成节点指针
        printf("%d %f %c\n", nodePtr->a, nodePtr->b, nodePtr->c); // 2.访问数据
    }

    // 释放链表
    linkPtr = to_link(&myList)->next;
    while (dstruct::_SinglyLink::empty(to_link(&myList))) {
        auto next = linkPtr->next;
        free(linkPtr);
        linkPtr = next;
    }

// example4
    /*{
        IntList intList;
        // build
        IntList_init(&intList);
        for (int i = 0; i < 10; i++) {
            // 分配内存
            IntList *node = (IntList *) malloc(sizeof(IntList));
            // 初始化
            node->data = i;
            // 添加到链表(头插法)
            IntList_add(&intList, node);
        }

        // access
        for (IntList *node = intList.next; node != &intList; node = node->next) {
            printf("%d\n", node->data);
        }

        // release
        while (!IntList_empty(&intList)) {
            IntList *node = intList.next;
            intList.next = node->next;
            free(node);
        }
    }*/
    {
        dstruct::SLinkedList<int> intList;

        // build
        for (int i = 0; i < 10; i++) {
            intList.push_back(i);
        }

        // access
        for (auto v : intList) {
            printf("%d\n", v);
        }

        // auto-release memory
        // ...
    }
    {
        struct IntList {
            dstruct::_SinglyLink linker;
            int data;
        };

        dstruct::_SinglyLink intList;

        // build
        dstruct::_SinglyLink::init(&intList);
        for (int i = 0; i < 10; i++) {
            // 分配内存
            IntList *node = (IntList *) malloc(sizeof(IntList));
            node->data = i; // 初始化
            // 添加到链表(头插法)
            dstruct::_SinglyLink::add(&intList, to_link(node));
        }

        // access
        for (auto *linkPtr = intList.next; linkPtr != &intList; linkPtr = linkPtr->next) {
            IntList *node = to_node(linkPtr, IntList, linker);
            printf("%d\n", node->data);
        }

        // release
        while (!dstruct::_SinglyLink::empty(&intList)) {
            IntList *node = to_node(intList.next, IntList, linker);
            intList.next = node->linker.next;
            free(node);
        }
    }
    return 0;
}



