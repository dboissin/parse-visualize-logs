#ifndef H_RANGES
#define H_RANGES

#include <stdlib.h>
#include <string.h>

typedef struct range {
  char* key;
  int staticCount;
  int upstreamCount;
  int errCount;
  float staticRtSum;
  float upstreamRtSum;
  float errRtSum;
  struct range * next;
} Range;

typedef struct ranges {
  Range* head;
  Range* last;
} Ranges;

Ranges* createRangesList();

void destroyRangesList(Ranges* list);

/* return next item */
Range* removeRange(Range* item);

Range* newRange(Ranges* list, char* rangeKey);

Range* getRange(Ranges *list, char *key);

Range* getRangeCreateIfNotExists(Ranges *list, char *key);

#endif
