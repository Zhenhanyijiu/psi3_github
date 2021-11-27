#include <stdio.h>
int main()
{
    unsigned char c1 = 0x3f;
    unsigned char c2 = 0x38;
    unsigned char c3 = 0x5d;
    unsigned char tmp = 0;
    tmp = c1 & (c2 ^ c3);
    printf("===tmp:%x\n", tmp);
    tmp = (c1 & c2) ^ (c1 & c3);
    printf("===tmp:%x\n", tmp);
    return 0;
}