#ifndef __HELLO_AOSP_API_H_
#define __HELLO_AOSP_API_H_

extern "C" int add(int a, int b);
using add_type = int (*) (int, int);

int max(int a, int b);

#endif