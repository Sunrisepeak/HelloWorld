# C++多版本库隐式间接引用的风险

一个项目对同一个库(mylib)不同版本存在**隐式间接引用关系**
导致其他开发者使用mylib时, 存在引发隐式ABI不兼容的风险

```cpp
      _ libtest -> mylib.v1
     /
main
     \_ mylib.v2
```

**构建示例**
```
bash build.sh
./main
```

**预期输出**
```text
version 1: 1000
Header-Only: version 2: 1000
Header-Only: version 1 ****
Header-Only: version 2: 20000
version 1: 20000
main: mylib-v1/mylib.cpp:8: void send(int): Assertion `val < 10000' failed.
Aborted (core dumped)
```

**环境**

```text
g++ (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Copyright (C) 2021 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```