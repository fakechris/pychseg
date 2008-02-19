#include <Python.h>
#include <stdio.h> /* C header files */
#include <stdlib.h>
#include <string.h>

static PyObject* is_basic_latin(PyObject* self, PyObject* args) 
{ 
	Py_UNICODE  *src;
	int srclen;
	register Py_UNICODE ch;

	if (! PyArg_ParseTuple(args, "u#", &src, &srclen))
		return NULL;

	if (srclen< 1) {
		return PyBool_FromLong(0);
	}

	ch = *src;
		
	if ( (ch >= 0x20 && ch <=0x7f) ) /* || (ch >= 0xff01 && ch <= 0xff5e) ) */	
		return PyBool_FromLong(1);
	else
		return PyBool_FromLong(0);	
} 

static PyMethodDef charutilsMethods[] =
{ 
   {"is_basic_latin",  is_basic_latin, METH_VARARGS, "is basic latin word?"},  
   {NULL, NULL, 0, NULL}
}; 

PyMODINIT_FUNC initcharutils(void) 
{ 
       Py_InitModule("charutils", charutilsMethods); 
} 
