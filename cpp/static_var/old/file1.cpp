#include <StaticVar.hpp>

static int static_var = 1;

int StaticVarInClass::member = 1;

void * file1_static_var() {
    return &static_var;
}

void * hpp_static_var_by_file1() {
    return &hpp_static_var;
}

void * hpp_static_function_by_file1() {
    return (void *)static_var_in_function;
}

void * hpp_StaticVarInClass_member_by_file1() {
    return &(StaticVarInClass::member);
}

void * hpp_static_var_in_function_by_file1() {
    return & static_var_in_function();
}

void * hpp_StaticVarInClass_member_func_by_file1() {
    return (void *)(StaticVarInClass::getInstance);
}

void * hpp_StaticVarInClass_func_by_file1() {
    return & StaticVarInClass::getInstance();
}

void * namespace_file1() {
    return & temp::namespace_static_var;
}