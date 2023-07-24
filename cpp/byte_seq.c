#include <stdio.h>

int main() {
	unsigned short val = 0x1122;
	printf("%p, %x\n", &val, *(unsigned char *)(&val));
	return 0;
}
