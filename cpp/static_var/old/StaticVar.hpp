#ifndef STATIC_VAR_HPP
#define STATIC_VAR_HPP

static int hpp_static_var = 1;

static int & static_var_in_function() {
    static int var = 1;
    return var;
}

namespace temp {

static int namespace_static_var = 1;

}

class StaticVarInClass {
public:
    static StaticVarInClass & getInstance() {
        static StaticVarInClass var;
        return var;
    }

    const static int var { 1 };

    static int member;

private:
    StaticVarInClass() = default;
};

// multiple definition of `StaticVarInClass::member';
// int StaticVarInClass::member = 1;

// file1.cpp
void * file1_static_var();
void * hpp_static_var_by_file1();
void * hpp_static_function_by_file1();
void * hpp_static_var_in_function_by_file1();
void * hpp_StaticVarInClass_func_by_file1();
void * hpp_StaticVarInClass_member_func_by_file1();
void * hpp_StaticVarInClass_member_by_file1();
void * namespace_file1();

// file2.cpp
void * file2_static_var();
void * hpp_static_var_by_file2();
void * hpp_static_function_by_file2();
void * hpp_static_var_in_function_by_file2();
void * hpp_StaticVarInClass_func_by_file2();
void * hpp_StaticVarInClass_member_func_by_file2();
void * hpp_StaticVarInClass_member_by_file2();
void * namespace_file2();

#endif