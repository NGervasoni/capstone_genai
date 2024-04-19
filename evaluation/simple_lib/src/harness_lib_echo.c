    #include "library.h"
    #include <stdint.h>
    #include <stdlib.h>
    
    int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
      char *data = (char *)Data;
      lib_echo(data, Size);
      return 0;
    }