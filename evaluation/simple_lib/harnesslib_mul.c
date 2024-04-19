    #include <stdint.h>
    #include <stdlib.h>
    #include "library.h"
    
    int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    	lib_mul(Data[0], Data[1]);
    	return 0;
    }