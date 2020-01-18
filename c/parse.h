#ifndef H_PARSE
#define H_PARSE

#include <stdio.h>
#include <stdint.h>
#include <zlib.h>
#include <python3.5m/Python.h>
#include "ranges.h"

#define BUFF_LENGTH 4096
#define DATE_RANGE_LENGTH 16
#define ERROR_CODE_LIMIT 399

PyObject * parse(PyObject *self, PyObject *args);

#endif