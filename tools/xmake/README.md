# xmake: C/C++轻量级构建和包管理工具 - 初步上手

## step0 - 快速安装

**linux/macos**

```bash
curl -fsSL https://xmake.io/shget.text | bash
```

**windows**

```bash
Invoke-Expression (Invoke-Webrequest 'https://xmake.io/psget.text' -UseBasicParsing).Content
```

> 注: 不能直接在cmd窗口执行, 需要在PowerShell窗口执行

更多安装细节见[官方文档](https://xmake.io/#/zh-cn/guide/installation)

## step1 - 常用命令

### 工程结构

**目录结构**

原始目录结构

```bash
.
├── src # 源码目录
│   └── main.cpp
└── xmake.lua # xmake项目构建描述文件

1 directory, 2 files

```

**工程构建描述文件xmake.lua**

```lua
target("main")
    add_files("src/main.cpp")
```

**演示代码**
```cpp
#include <iostream>

bool test() {
    int *ptr = nullptr;
    *ptr = 0; // test
    return true;
}

int main() {
    std::cout << "Hello xmake!" << std::endl;
    test();
    return 0;
}
```


### 常用命令

**构建**
```lua
xmake build <target_name>
```
或
```lua
xmake
```

`<target_name>`: 用于指定要构建的目标, 省略表示构建所有目标

**构建后目录结构**

```bash
.
├── build
├── src
│   └── main.cpp
├── .xmake
└── xmake.lua
```

构建后会多出两个目录
- `build`: 存放构建产物(obj目标文件/动态库/可执行文件...)
- `.xmake`: 存放和项目相关的配置缓存

> 注: 当只使用`xmake`进行构建的时候表示构建所有项目, 并且可以加上`-v`参数可以显示构建细节

**清理构建产物**

```lua
xmake c
```

**运行目标**
```lua
xmake r <target_name>
```

`<target_name>`: 用于指定xmake.lua中描述的目标规则

### debug模式和程序调试

```lua
add_rules("mode.debug", "mode.release")
```
> 注: 使用debug功能的时候, 最好在xmake.lua开头添加规则描述, 否则可能不能正确生成可调试程序

**xmake f -m <release|debug>**

```lua
xmake f -m release
```
```bash
[ 25%]: cache compiling.release src/main.cpp
[ 50%]: linking.release main
[100%]: build ok, spent 0.068s
```

```lua
--- xmake config -m debug
xmake f -m debug
```
```bash
[ 25%]: cache compiling.debug src/main.cpp
[ 50%]: linking.debug main
[100%]: build ok, spent 0.055s
```

可以使用`xmake f -m <mode>`进行切换相关的构建模式
并且可以通过xmake构建输出信息(`[ 50%]: linking.release main`)区分当前所处于的模式
在处于`debug`模式下, 可以直接使用xmake对程序进行调试(它会自动的检测调试器并配置)

```lua
xmake r -d <target_name>
```

在运行的时候增加`-d`选项, 就会进入调试模式

```bash
speak@speak-pc:~/workspace/github/HelloWorld/tools/xmake/step1$ xmake f -m debug
checking for platform ... linux
checking for architecture ... x86_64
speak@speak-pc:~/workspace/github/HelloWorld/tools/xmake/step1$ xmake 
[ 50%]: cache compiling.debug src/main.cpp
[ 75%]: linking.debug main
[100%]: build ok, spent 0.227s
speak@speak-pc:~/workspace/github/HelloWorld/tools/xmake/step1$ xmake r -d main
GNU gdb (Ubuntu 12.1-0ubuntu1~22.04) 12.1
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from /home/speak/workspace/github/HelloWorld/tools/xmake/step1/build/linux/x86_64/debug/main...
(gdb) l
1       #include <iostream>
2
3       bool test() {
4           int *ptr = nullptr;
5           *ptr = 0; // test
6           return true;
7       }
8
9       int main() {
10          std::cout << "Hello xmake!" << std::endl;
(gdb)
```

## step2: 构建静态库和动态库

使用`set_kind`可以描述构建目标的类型

**构建静态库 - set_kind("static")**
```lua
add_includedirs("include")

target("xlib-static")
    set_kind("static")
    add_files("src/*.cpp")
```

**构建动态库 - set_kind("shared")**
```lua
target("xlib-shared")
    set_kind("shared")
    add_files("src/*.cpp")
```

**构建库测试程序 - set_kind("binary")**

```lua
target("test")
    set_kind("binary")
    add_files("tests/test.cpp")
    add_deps("xlib-shared")
```

使用`xmake build test`命令构建测试程序, 将会根据`add_deps("xlib-shared")`的描述自动构建相关库依赖


### 完成工程结构

```bash
.
├── include
│   └── xlib.h
├── src
│   ├── libinfo.cpp
│   └── xlib.cpp
├── tests
│   └── test.cpp
└── xmake.lua

3 directories, 5 files
```

**include/xlib.h**

```cpp
#ifndef __XLIB_H__
#define __XLIB_H__

void print_lib_info();
int add(int a, int b);

#endif
```

**src/libinfo.cpp**

```cpp
#include <iostream>

#include "xlib.h"

void print_lib_info() {
    std::cout << "xlib v1 - 2024/3/31" << std::endl;
}
```

**src/xlib.cpp**

```cpp
#include "xlib.h"

int add(int a, int b) {
    return a + b;
}
```

**test/test.cpp**

```cpp
#include <iostream>

#include "xlib.h"

int main() {
    print_lib_info();

    int sum = add(100, 200);
    std::cout << "sum: " << sum << std::endl;

    return 0;
}
```

**xmake.lua**

```lua
add_includedirs("include")

target("xlib-static")
    set_kind("static")
    add_files("src/*.cpp")

target("xlib-shared")
    set_kind("shared")
    add_files("src/*.cpp")

target("test")
    set_kind("binary")
    add_files("tests/test.cpp")
    add_deps("xlib-shared")
```


## step3 - 包管理/依赖和远程库引用

### xmake官方包管理和依赖

> 包管理仓库[xmake-repo](https://github.com/xmake-io/xmake-repo)


```lua
add_requires("gtest v1.11.0")

target("test")
    set_kind("binary")
    add_packages("gtest")
    add_files("dstruct_test.cpp")
```

通过`add_requires`增加项目的包依赖(其中指定版本号是可选的), 并通过`add_packages`给指定`target`进行配置

**自动处理库依赖 - gtest**
```bash
note: install or modify (m) these packages (pass -y to skip confirm)?
in xmake-repo:
  -> gtest v1.11.0 
please input: y (y/n/m)
y
  => download https://github.com/google/googletest/archive/refs/tags/v1.11.0.zip .. failed
  => clone https://github.com/google/googletest.git v1.11.0 .. ok
  => install gtest v1.11.0 .. ok
[ 50%]: cache compiling.release dstruct_test.cpp
[ 75%]: linking.release test
[100%]: build ok, spent 0.437s
```

### 个人项目包引用

```lua
package("dstruct")
    set_urls("git@github.com:Sunrisepeak/dstruct.git")

    add_includedirs(".")

    on_install(function (package)
        os.mv("*", package:installdir("."))
    end)
package_end()

add_requires("dstruct")
```

`package("dstruct")/package_end()`是用来描述包信息的, 上面这个模板适用于大部分`header-only`库

> 注: 也可以把你的包描述`package("YourLibName") / package_end()`上传到官方xmake-repo仓库, 这样就可以通过`add_requires`直接使用了。更多相关细节见文档[添加包到仓库](https://xmake.io/#/zh-cn/package/remote_package?id=%e6%b7%bb%e5%8a%a0%e5%8c%85%e5%88%b0%e4%bb%93%e5%ba%93)

- `set_urls`: 配置库的地址
- `add_includedirs`: 配置库中的头文件路径
- `on_install`: 用于描述安装库时的细节。如: 编译成静态库还是动态库, 以及需要安装哪些头文件等, 对于只有头文件的库直接`os.mv`或`os.cp`所有仓库文件即可

**自动处理个人(或私有)库依赖 - dstruct**

```bash
speak@speak-pc:~/workspace/github/HelloWorld/tools/xmake/step3$ xmake
checking for platform ... linux
checking for architecture ... x86_64
note: install or modify (m) these packages (pass -y to skip confirm)?
  -> dstruct @default 
please input: y (y/n/m)
y
  => clone git@github.com:Sunrisepeak/dstruct.git @default .. ok
  => install dstruct @default .. ok
[ 50%]: cache compiling.release dstruct_test.cpp
[ 75%]: linking.release test
[100%]: build ok, spent 0.59s
speak@speak-pc:~/workspace/github/HelloWorld/tools/xmake/step3$ xmake r
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from Vector
[ RUN      ] Vector.resize
[       OK ] Vector.resize (0 ms)
[----------] 1 test from Vector (0 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test suite ran. (0 ms total)
[  PASSED  ] 1 test.
```

### 完成工程结构

```bash
.
├── dstruct_test.cpp
└── xmake.lua

0 directories, 2 files
```

**xmake.lua**

```lua
add_requires("gtest v1.11.0")

package("dstruct")
    set_urls("git@github.com:Sunrisepeak/dstruct.git")

    add_includedirs(".")

    on_install(function (package)
        os.mv("*", package:installdir("."))
    end)
package_end()

add_requires("dstruct")

target("test")
    set_kind("binary")
    add_packages("gtest", "dstruct")
    add_files("dstruct_test.cpp")
```

**dstruct_test.cpp**

```cpp
#include <gtest/gtest.h>

#include <dstruct.hpp>

TEST(Vector, resize) {
    dstruct::Vector<int> vec;
    ASSERT_EQ(vec.size(), 0);
    vec.push_back(1);
    vec.resize(10, -1);
    ASSERT_EQ(vec.size(), 10);
    ASSERT_EQ(vec[0], 1);
    ASSERT_EQ(vec[1], -1);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
```

---

[HelloWorld项目](https://github.com/Sunrisepeak/HelloWorld)