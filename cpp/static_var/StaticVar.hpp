#ifndef __STATIC_VAR_HPP__
#define __STATIC_VAR_HPP__

static int hpp_static_var = 1;

static int & static_var_in_function() {
    static int var = 1;
    return var;
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

// file2.cpp
void * file2_static_var();
void * hpp_static_var_by_file2();
void * hpp_static_function_by_file2();
void * hpp_static_var_in_function_by_file2();
void * hpp_StaticVarInClass_func_by_file2();
void * hpp_StaticVarInClass_member_func_by_file2();
void * hpp_StaticVarInClass_member_by_file2();

#endif