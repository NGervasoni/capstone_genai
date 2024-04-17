#include <stdint.h>
#include <stdlib.h>
#include "library.h"

int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    char *data = (char *)Data;
    lib_echo4(data, Size);
    return 0;
}