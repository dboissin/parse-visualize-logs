#include <python3.5m/Python.h>
#include "parse.h"

PyMethodDef funcs[] = {
	{	"parse",
		(PyCFunction)parse,
		METH_VARARGS,
		"Parse nginx logs"
    },
	{	NULL}
};

PyModuleDef mod = {
	PyModuleDef_HEAD_INIT,
	"parse",
	"Parse logs module",
	-1,
	funcs,
	NULL,
	NULL,
	NULL,
	NULL
};

PyMODINIT_FUNC PyInit_parse(void) {
	return PyModule_Create(&mod);
}
