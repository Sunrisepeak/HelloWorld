#ifndef MYLIB_H
#define MYLIB_H

#include <cstdio>

#define HONLY_LOGD(...) { fprintf (stdout, "[LOGD]: \t%s: %s:%d - ", __func__, __FILE__, __LINE__); fprintf(stdout, __VA_ARGS__); printf("\n"); }

static int cnt = 0; // 改变

void mylib1_func();
void mylib2_func();

#endif