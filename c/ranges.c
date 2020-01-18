#include "ranges.h"

Ranges* createRangesList(void) {
    Ranges *ranges;
    ranges = malloc(sizeof(Ranges));
    ranges->head = 0;
    ranges->last = 0;
    return ranges;
}

void destroyRangesList(Ranges *ranges) {
    Range *range;
    if (ranges != NULL) {
        range = ranges->head;
        while (range != NULL) {
            range = removeRange(range);
        }
        free(ranges);
    }
}

Range* removeRange(Range *range) {
    Range *next;
    next = range->next;
    if (range->key != NULL) {
        free(range->key);
    }
    free(range);
    return next;
}

Range* newRange(Ranges *ranges, char *key) {
    Range *range;
    char *k;
    int len;
    range = malloc(sizeof(Range));
    range->staticCount = 0;
    range->upstreamCount = 0;
    range->errCount = 0;
    range->staticRtSum = 0;
    range->upstreamRtSum = 0;
    range->errRtSum = 0;
    len = strlen(key) + 1;
    k = (char *) malloc(sizeof(char) * len);
    strcpy(k, key);
    range->key = k;
    range->next = ranges->head;
    if (ranges->last == NULL) {
        ranges->last = range;
    }
    ranges->head = range;
    return range;
}

Range* getRange(Ranges *ranges, char *key) {
    Range *range;
    if (ranges != NULL) {
        range = ranges->head;
        while (range != NULL) {
            if (strcmp(key, range->key) == 0) {
                return range;
            }
            range = range->next;
        }
    }
    return NULL;
}

Range* getRangeCreateIfNotExists(Ranges *ranges, char *key) {
    Range* range;
    range = getRange(ranges, key);
    if (range == NULL) {
        range = newRange(ranges, key);
    }
    return range;
}
