#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <libxml/xmlmemory.h>
#include <libxml/parser.h>

int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    xmlDocPtr doc = xmlReadFile((const char *)Data, NULL, XML_PARSE_NOBLANKS);
    if (doc == NULL) {
        return 0;
    }

    // Step 3: parse the XML document and extract the information you need
    // (e.g. using the `xmlNodeListGetString` function)
    // ...

    xmlFreeDoc(doc);
    return 0;
}