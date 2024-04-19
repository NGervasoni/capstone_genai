#include <stdint.h>
#include <libxml/xmlmemory.h>
#include <libxml/parser.h>

int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    xmlReadFile((const char *)Data, (const char *)Size, NULL, NULL, 0);
    return 0;
}