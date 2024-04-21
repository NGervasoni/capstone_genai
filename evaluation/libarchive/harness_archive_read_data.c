#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <archive.h>
#include <archive_entry.h>

int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    struct archive *ina;
    struct archive_entry *entry;
    char buff[8192];
    ssize_t len;
    int r;

    ina = archive_read_new();
    if (ina == NULL) {
        return 0;
    }

    if (archive_read_support_filter_all(ina) != ARCHIVE_OK) {
        return 0;
    }

    if (archive_read_support_format_all(ina) != ARCHIVE_OK) {
        return 0;
    }

    if (archive_read_open_fd(ina, 0, 10240) != ARCHIVE_OK) {
        return 0;
    }

    while ((r = archive_read_next_header(ina, &entry)) == ARCHIVE_OK) {
        len = archive_read_data(ina, buff, sizeof(buff));
        if (len < 0) {
            return 0;
        }
    }

    if (r != ARCHIVE_EOF) {
        return 0;
    }

    archive_read_free(ina);

    return 0;
}