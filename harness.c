#include <stdint.h>
#include <stdlib.h>
#include "library.h"

int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    // Step 3: call lib_echo with the input data
    lib_echo((char *)Data, Size);
    return 0;
}