#include "parse.h"

Ranges *parseFile(char *path) {
    FILE *fp;
    char line[BUFF_LENGTH];
    Range *currRange;
    char statusCode[4];
    char rt[6];
    char currDate[DATE_RANGE_LENGTH + 1];
    Ranges *ranges;
    char *dateIdx, *rtIdx, *statusIdx, *urtIdx;

    ranges = createRangesList();
    currDate[DATE_RANGE_LENGTH] = '\0';
    statusCode[3] = '\0';
    rt[5] = '\0';

    fp = fopen(path, "rt");
    while (fgets(line, BUFF_LENGTH, fp) != NULL) {
        dateIdx = strchr(line, '[') + 1;
        rtIdx = strstr(line, "\"rt=") + 4;
        statusIdx = strstr(line, "\" ") + 2;

        strncpy(currDate, dateIdx, DATE_RANGE_LENGTH);
        currRange = getRangeCreateIfNotExists(ranges, currDate);

        strncpy(rt, rtIdx, 5);

        strncpy(statusCode, statusIdx, 3);
        if (atoi(statusCode) > ERROR_CODE_LIMIT) {
            currRange->errCount++;
            currRange->errRtSum += atof(rt);
        } else {
            urtIdx = strstr(line, "urt=\"") + 5;
            if (*urtIdx == '-') {
                currRange->staticCount++;
                currRange->staticRtSum += atof(rt);
            } else {
                currRange->upstreamCount++;
                currRange->upstreamRtSum += atof(rt);
            }
        }
    }
    fclose(fp);

    return ranges;
}

PyObject * parse(PyObject *self, PyObject *args) {
	char *path;
    Ranges *ranges;

	if(!PyArg_ParseTuple(args, "s", &path)) {
		return NULL;
    }

    ranges = parseFile(path);

    PyObject* dict = PyDict_New();

    Range * range = ranges->head;
    while (range != NULL) {
        PyObject* d = PyDict_New();
        PyDict_SetItemString(d, "upstream_count", Py_BuildValue("i", range->upstreamCount));
        PyDict_SetItemString(d, "static_count", Py_BuildValue("i", range->staticCount));
        PyDict_SetItemString(d, "err_count", Py_BuildValue("i", range->errCount));
        PyDict_SetItemString(d, "upstream_rt_sum", Py_BuildValue("f", range->upstreamRtSum));
        PyDict_SetItemString(d, "static_rt_sum", Py_BuildValue("f", range->staticRtSum));
        PyDict_SetItemString(d, "err_rt_sum", Py_BuildValue("f", range->errRtSum));
        PyDict_SetItemString(dict, range->key, d);
        range = range->next;
    }

    destroyRangesList(ranges);

	return Py_BuildValue("O", dict);
}

/*
int main(int argc, char **argv) {
    Range* range;
    Ranges* ranges;
    ranges = parseFile("logs/access.log");
    range = ranges->head;
    while (range != NULL) {
        printf("%s,%d,%f,%d,%f,%d,%f\n",
            range->key, range->upstreamCount, range->upstreamRtSum,
            range->staticCount, range->staticRtSum, range->errCount,
            range->errRtSum);
        range = range->next;
    }

    destroyRangesList(ranges);
    return 0;
}
*/