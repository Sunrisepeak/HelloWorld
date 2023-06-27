#include <stdio.h>

typedef int (*ReturnType)(int arg1);
typedef ReturnType (*FuncPtr)(int arg1, int arg2);


int add1(int arg1) {
	return 1 + arg1;
}

int add2(int arg1) {
	return 2 + arg1;
}

ReturnType func2(int arg1, int arg2) {
	if (arg1 == arg2) {
		return add1;
	}
	return add2;
}

int main() {

	FuncPtr f2Ptr;   // 需求
	ReturnType f1Ptr;

// test0: 赋值测试
	f2Ptr = func2;

// test1: 调用测试1, 获取add1
	f1Ptr = f2Ptr(1, 1);
	printf("f2Ptr(1, 1): f1Ptr -> add1 %d\n", f1Ptr(0));

// test2: 调用测试2, 获取add2
	f1Ptr = f2Ptr(1, 2);
	printf("f2Ptr(1, 2): f1Ptr -> add2 %d\n", f1Ptr(0));

	return 0;
}

