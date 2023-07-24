#define LOG_TAG "max"

#include <log/log.h>

#include "helloaosp.h"

int max(int a, int b) {
	int c = a > b ? a : b;
	ALOGD("return %d", c);
	return c;
}