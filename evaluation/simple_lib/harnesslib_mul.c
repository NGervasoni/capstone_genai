#include <stdint.h>
#include <stdlib.h>
#include "src/library.h"

int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    // Step 3: call lib_mul with the input data
    int result = lib_mul(Data[0], Data[1]);
    // Step 4: return the result
    return result;
}