#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <libxml/xmlmemory.h>
#include <libxml/parser.h>

int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    xmlDocPtr doc;
    xmlNodePtr root;

    doc = xmlReadMemory((const char *)Data, Size, "noname.xml", NULL, 0);
    if (doc == NULL) {
        return 0;
    }

    root = xmlDocGetRootElement(doc);
    if (root == NULL) {
        xmlFreeDoc(doc);
        return 0;
    }

    xmlFreeDoc(doc);
    return 0;
}