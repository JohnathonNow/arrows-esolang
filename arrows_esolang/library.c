#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int* lstack = 0;
int* rstack = 0;
int lsize = 1024;
int rsize = 1024;
int l_index = 0;
int r_index = 0;

void init() {
    lstack = malloc(sizeof(int)*lsize);
    rstack = malloc(sizeof(int)*rsize);
}

void lpush(int x) {
    if (!lstack) {
        init();
    }
    lstack[l_index++] = x;
    if (l_index >= lsize) {
        int* old = lstack;
        lstack = malloc(sizeof(int)*lsize*2);
        memcpy(lstack, old, lsize);
        lsize *= 2;
        free(old);
    }
}

void rpush(int x) {
    if (!rstack) {
        init();
    }
    rstack[r_index++] = x;
    if (r_index >= rsize) {
        int* old = rstack;
        rstack = malloc(sizeof(int)*rsize*2);
        memcpy(rstack, old, rsize);
        rsize *= 2;
        free(old);
    }
}

int lpop() {
    lstack[l_index] = 0;
    if (--l_index < 0) {
        l_index = 0;
    }
    return lstack[l_index];
}

int rpop() {
    rstack[r_index] = 0;
    if (--r_index < 0) {
        r_index = 0;
    }
    return rstack[r_index];
}

int libgetchar() {
    int c = getchar();
    if (c == EOF) {
        c = 0;
    }
    return c;
}
