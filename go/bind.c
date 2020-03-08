#include <python3.5m/Python.h>

int PyArg_ParseTuple_S(PyObject * args, char** a) {
	return PyArg_ParseTuple(args, "s", a);
}

PyObject * Py_BuildValue_I(int a) {
	return Py_BuildValue("i", a);
}

PyObject * Py_BuildValue_F(float a) {
	return Py_BuildValue("f", a);
}

PyObject * Py_BuildValue_S(char* s) {
	return Py_BuildValue("s", s);
}

PyObject * parse(PyObject *, PyObject *);

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
