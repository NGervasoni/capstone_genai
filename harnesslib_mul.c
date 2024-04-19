#include <stdint.h>
#include <stdlib.h>
#include "library.h"

int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    char *data = (char *)Data;
    ssize_t len = Size;
    lib_echo(data, len);
    return 0;
}