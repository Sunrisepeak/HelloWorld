#include <cstdio>

#include <StaticVar.hpp>

/*
struct A {
    using Type = int &;
    operator int&() {
        printf("%p\n", &i);
        return i;
    }

    int i;
};

void test(int &i) {
    i = 2;
}
*/
int main() {
    //A a;
    //test(a);
    //printf("%p %d\n", &a, a.i);

    return 0;

    printf("file1: static var %p\n", file1_static_var());
    printf("file2: static var %p\n", file2_static_var());

    printf("\n");

    printf("hpp: static var %p\n", &hpp_static_var);
    printf("file1: hpp: static var %p\n", hpp_static_var_by_file1());
    printf("file2: hpp: static var %p\n", hpp_static_var_by_file2());

    printf("\n");

    printf("hpp: static function %p\n", static_var_in_function);
    printf("file1: hpp: static function %p\n", hpp_static_function_by_file1());
    printf("file2: hpp: static function %p\n", hpp_static_function_by_file2());

    printf("\n");

    printf("hpp: static var in function %p\n", & (static_var_in_function()));
    printf("file1: hpp: static var in function %p\n", hpp_static_var_in_function_by_file1());
    printf("file2: hpp: static var in function %p\n", hpp_static_var_in_function_by_file2());

    printf("\n");

    printf("hpp: static class var %p\n", & (StaticVarInClass::getInstance()));
    printf("file1: hpp: static class var %p\n", hpp_StaticVarInClass_func_by_file1());
    printf("file2: hpp: static class var %p\n", hpp_StaticVarInClass_func_by_file2());

    printf("\n");

    printf("hpp: static class member function %p\n", StaticVarInClass::getInstance);
    printf("file1: hpp: static class member function %p\n", hpp_StaticVarInClass_member_func_by_file1());
    printf("file2: hpp: static class member function %p\n", hpp_StaticVarInClass_member_func_by_file2());

    printf("\n");

    printf("file1: hpp: static class var %p\n", hpp_StaticVarInClass_member_by_file1());
    printf("file2: hpp: static class var %p\n", hpp_StaticVarInClass_member_by_file2());

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