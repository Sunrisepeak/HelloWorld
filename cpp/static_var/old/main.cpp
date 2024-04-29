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

/*

g++ -I cpp/static_var/  cpp/static_var/main.cpp cpp/static_var/file1.cpp cpp/static_var/file2.cpp

g++ (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Copyright (C) 2021 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

file1: static var 0x561117e98020
file2: static var 0x561117e98030

hpp: static var 0x561117e98010
file1: hpp: static var 0x561117e98018
file2: hpp: static var 0x561117e98028

hpp: static function 0x561117e95169
file1: hpp: static function 0x561117e953f0
file2: hpp: static function 0x561117e95474

hpp: static var in function 0x561117e98014
file1: hpp: static var in function 0x561117e9801c
file2: hpp: static var in function 0x561117e9802c

hpp: static class var 0x561117e98035
file1: hpp: static class var 0x561117e98035
file2: hpp: static class var 0x561117e98035

hpp: static class member function 0x561117e953df
file1: hpp: static class member function 0x561117e953df
file2: hpp: static class member function 0x561117e953df

file1: hpp: static class var 0x561117e98024
file2: hpp: static class var 0x561117e98024

*/