/*
gcc (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0
Copyright (C) 2019 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

gcc array-and-pointer.c && ./a.out

*/


#include <assert.h>

int test1() {
// test0: 初始化
    char str1[10] = "Hello";  // char数组
    char *str2 = "Hello";     // char指针

    assert(str2 != str1);    // 不等断言
    str2 = str1;

// test1: 数组(下标)访问方式
    for (int i = 0; i < 10; i++) {
        //str1[i] = '0' + i;
        str2[i] = '0' + i;
        assert(str1[i] == str2[i]); // 相等断言 
    }

// test2: 赋值
    // str1 = "helloworld"; error
    str2 = "0123456789";

    assert(str2 != str1);           // 不等断言

// test3: 指针(+偏移)访问方式
    for (int i = 0; i < 10; i++) {
        assert(*(str1 + i) == *(str2 + i));  // 相等断言
    }
}

int test2() {
    char str1[10];  // char数组
    char *str2;     // char指针

    // str1 = "helloworld"; error
    str2 = "0123456789";

    str1[0] = 'a';
    str2 = str1;

/*
; https://gcc.godbolt.org/
; x86-64 gcc 10.1

.LC0:
        .string "0123456789"
test2:
        push    rbp
        mov     rbp, rsp
        lea     rax, [rbp-18]
        mov     QWORD PTR [rbp-8], rax
        mov     QWORD PTR [rbp-8], OFFSET FLAT:.LC0
        nop
        pop     rbp
        ret
*/
}

int main() {
    test1();
    test2();
    return 0;
}