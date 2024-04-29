# C/C++: 多文件静态变量作用域的X种情况?



## 基本概念

- 局部静态变量
- 全局静态变量
- **作用域受文件限制**
- 共享属性



由于静态变量**作用域受文件限制**的原因, 就可能会导致一些使用上的一些问题, 下面就来对一些使用情况进行简单测试和分析

```cpp
speak@speak-pc:~$ g++ --version
g++ (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Copyright (C) 2021 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```



## 情况一 : 单cpp文件内的局部变量

### 测试代码

**main.cpp**

```cpp
#include <cstdio>

int count() {
    static int cnt = 0;
    return ++cnt;
}

int main() {
    printf("count: %d\n", count());
    printf("count: %d\n", count());
    return 0;
}
```

### 测试结果

```bash
count: 1
count: 2
```



局部变量cnt, 只会在第一次调用时初始化一次, 且只存一份



## 情况二 : 多cpp文件内的同名全局静态变量

### 测试代码

**mylib.h**

```cpp
#ifndef MYLIB_H
#define MYLIB_H

#include <cstdio>

#define HONLY_LOGD(...) { fprintf (stdout, "[LOGD]: \t%s: %s:%d - ", __func__, __FILE__, __LINE__); fprintf(stdout, __VA_ARGS__); printf("\n"); }

void mylib1_func();
void mylib2_func();

#endif
```

**mylib1.cpp**

```cpp
#include "mylib.h"

static int cnt = 1;

void mylib1_func() {
    HONLY_LOGD("cnt %d, addr %p", cnt, &cnt);
}
```

**mylib2.cpp**

```cpp
#include "mylib.h"

static int cnt = 2;

void mylib2_func() {
    HONLY_LOGD("cnt %d, addr %p", cnt, &cnt);
}
```

**main.cpp**

```cpp
#include <mylib.h>

int main() {
    mylib1_func();
    mylib2_func();
    return 0;
}
```

### 测试结果

```bash
[LOGD]:         mylib1_func: test2/mylib1.cpp:6 - cnt 1, addr 0x5843e71f0010
[LOGD]:         mylib2_func: test2/mylib2.cpp:6 - cnt 2, addr 0x5843e71f0014
```



不同文件中的静态变量的地址不相同

由于静态变量作用域受文件限制, 所以不同.cpp文件里的同名全局静态变量本质是两个不同的变量



## 情况三 : 头文件的中的全局静态变量

### 测试代码

> 主要是把分别定义在两个文件中的cnt删除, 改成在头文件中定义

```cpp
#ifndef MYLIB_H
#define MYLIB_H

#include <cstdio>

#define HONLY_LOGD(...) { fprintf (stdout, "[LOGD]: \t%s: %s:%d - ", __func__, __FILE__, __LINE__); fprintf(stdout, __VA_ARGS__); printf("\n"); }

static int cnt = 0;

void mylib1_func();
void mylib2_func();

#endif


// mylib1.cpp
#include "mylib.h"

void mylib1_func() {
    HONLY_LOGD("cnt %d, addr %p", cnt, &cnt);
}

// mylib2.cpp
#include "mylib.h"

void mylib2_func() {
    HONLY_LOGD("cnt %d, addr %p", cnt, &cnt);
}
```

### 测试结果

```cpp
[LOGD]:         mylib1_func: test3/mylib1.cpp:4 - cnt 0, addr 0x63cf88c6901c
[LOGD]:         mylib2_func: test3/mylib2.cpp:4 - cnt 0, addr 0x63cf88c69020
```



cnt是不同的地址?

因为在一个同文件中定义一个全局静态变量, 等同在每一个包含这个头文件的cpp文件中分别定义一个全局静态变量, 也就是等同于情况二



### 情况四 : 头文件中函数里的静态变量

### 测试代码

> 头文件中定义一个mylib返回局部静态变量cnt的地址

```cpp
#ifndef MYLIB_H
#define MYLIB_H

#include <cstdio>

#define HONLY_LOGD(...) { fprintf (stdout, "[LOGD]: \t%s: %s:%d - ", __func__, __FILE__, __LINE__); fprintf(stdout, __VA_ARGS__); printf("\n"); }

static void * mylib() {
    static int cnt = 0;
    return &cnt;
}

void mylib1_func();
void mylib2_func();

#endif


// mylib1.cpp
#include "mylib.h"

void mylib1_func() {
    HONLY_LOGD("cnt: addr %p", mylib());
}

// mylib2.cpp
#include "mylib.h"

void mylib2_func() {
    HONLY_LOGD("cnt: addr %p", mylib());
}

// main.cpp
#include <mylib.h>

int main() {
    mylib1_func();
    mylib2_func();
    mylib1_func();
    mylib2_func();
    return 0;
}
```

## 测试结果

```cpp
[LOGD]:         mylib1_func: test4/mylib1.cpp:4 - cnt: addr 0x5adb0811b01c
[LOGD]:         mylib2_func: test4/mylib2.cpp:4 - cnt: addr 0x5adb0811b020
[LOGD]:         mylib1_func: test4/mylib1.cpp:4 - cnt: addr 0x5adb0811b01c
[LOGD]:         mylib2_func: test4/mylib2.cpp:4 - cnt: addr 0x5adb0811b020
```

同文件调用mylib获取的地址一样, 文件不同地址不一样

由于编译器在预处理时候, 会直接导入cpp文件中的`#include`的文件, 就导致每个文件中都定义了一个静态属性的`mylib`函数, 又加上静态属性作用域的文件隔离特性, 形成了这种情况

```cpp
// g++ -E test4/mylib1.cpp

# 8 "test4/mylib.h"
static void * mylib() {
    static int cnt = 0;
    return &cnt;
}

void mylib1_func();
void mylib2_func();
# 2 "test4/mylib1.cpp" 2

void mylib1_func() {
    { fprintf (
# 4 "test4/mylib1.cpp" 3 4
   stdout
# 4 "test4/mylib1.cpp"
   , "[LOGD]: \t%s: %s:%d - ", __func__, "test4/mylib1.cpp", 4); fprintf(
# 4 "test4/mylib1.cpp" 3 4
   stdout
# 4 "test4/mylib1.cpp"
   , "cnt: addr %p", mylib()); printf("\n"); };
}
```



## 情况五 : 头文件中类成员函数里的静态变量

### 测试代码

```cpp
#ifndef MYLIB_H
#define MYLIB_H

#include <cstdio>

#define HONLY_LOGD(...) { fprintf (stdout, "[LOGD]: \t%s: %s:%d - ", __func__, __FILE__, __LINE__); fprintf(stdout, __VA_ARGS__); printf("\n"); }

class Test {
public:
    static void * mylib() {
        static int cnt = 0;
        return &cnt;
    }

    //static int mVar;
};

void mylib1_func();
void mylib2_func();

#endif

// mylib1.cpp
#include "mylib.h"

void mylib1_func() {
    HONLY_LOGD("cnt: addr %p", Test::mylib());
}

// mylib2.cpp
#include "mylib.h"

void mylib2_func() {
    HONLY_LOGD("cnt: addr %p", Test::mylib());
}
```

### 测试结果

```cpp
[LOGD]:         mylib1_func: test5/mylib1.cpp:4 - cnt: addr 0x56486394a01c
[LOGD]:         mylib2_func: test5/mylib2.cpp:4 - cnt: addr 0x56486394a01c
[LOGD]:         mylib1_func: test5/mylib1.cpp:4 - cnt: addr 0x56486394a01c
[LOGD]:         mylib2_func: test5/mylib2.cpp:4 - cnt: addr 0x56486394a01c
```

地址全都一样了

熟悉的朋友, 已经看出了这是C++中类单例的使用方法
同时这也是header-only库定义全局共享静态变量的一种思路, 可以避免类静态成员变量的初始化问题

