    #include "library.h"
    #include <stdint.h>
    #include <stdlib.h>
    
    int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
      int x = *(int *)(Data);
      int y = *(int *)(Data + sizeof(int));
      lib_mul(x, y);
      return 0;
    }