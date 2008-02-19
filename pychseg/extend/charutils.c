#include <Python.h>
#include <stdio.h> /* C header files */
#include <stdlib.h>
#include <string.h>

static PyObject* is_basic_latin(PyObject* self, PyObject* args) 
{ 
	PyObject *result;
	Py_UNICODE  *src;
	int srclen, i;

	if (! PyArg_ParseTuple(args, "u", &src))
		return NULL;

	srclen = strlen(src);
	assert(srclen == 1);
	
	//i = ord(src);
	
	printf("%d\n", srclen);
	
	Py_RETURN_TRUE; 
	
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
