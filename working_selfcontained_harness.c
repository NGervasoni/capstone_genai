#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>
#include <unistd.h>

// #include "library.h"

void lib_echo(char *data, ssize_t len){
	if(strlen(data) == 0) {
		return;
	}
	char *buf = calloc(1, len);
	strncpy(buf, data, len);
	printf("%s",buf);
	free(buf);

	// A crash so we can tell the harness is working for lib_echo
	if(data[0] == 'p') {
		if(data[1] == 'o') {
			if(data[2] =='p') {
				if(data[3] == '!') {
					assert(0);
				}
			}
		}
	}
}

int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    char *data = (char *)Data;
    lib_echo(data, Size);
    return 0;
}