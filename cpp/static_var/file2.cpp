#include <StaticVar.hpp>

static int static_var = 1;

// multiple definition of `StaticVarInClass::member'
//int StaticVarInClass::member = 1;

void * file2_static_var() {
    return &static_var;
}

void * hpp_static_var_by_file2() {
    return &hpp_static_var;
}

void * hpp_static_function_by_file2() {
    return (void *)static_var_in_function;
}

void * hpp_StaticVarInClass_member_by_file2() {
    return &(StaticVarInClass::member);
}

void * hpp_static_var_in_function_by_file2() {
    return & static_var_in_function();
}

void * hpp_StaticVarInClass_member_func_by_file2() {
    return (void *)(StaticVarInClass::getInstance);
}

void * hpp_StaticVarInClass_func_by_file2() {
    return & StaticVarInClass::getInstance();
}