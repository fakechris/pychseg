%module pydarts

// This tells SWIG to treat char ** as a special case
%typemap(in) char ** {
  /* Check if is a list */
  if (PyList_Check($input)) {
    int size = PyList_Size($input);
    int i = 0;
    $1 = (char **) malloc((size+1)*sizeof(char *));
    for (i = 0; i < size; i++) {
      PyObject *o = PyList_GetItem($input,i);
      if (PyString_Check(o))
	$1[i] = PyString_AsString(PyList_GetItem($input,i));
      else {
	PyErr_SetString(PyExc_TypeError,"list must contain strings");
	free($1);
	return NULL;
      }
    }
    $1[i] = 0;
  } else {
    PyErr_SetString(PyExc_TypeError,"not a list");
    return NULL;
  }
}

// This cleans up the char ** array we malloc'd before the function call
%typemap(freearg) char ** {
  free((char *) $1);
}

%{
#include "darts.h"
%}


namespace Darts {
  template  <class key_type,  class node_u_type_,
             class value_type, class array_u_type_,
             class length_func_ = Length<key_type> >
  class DoubleArrayImpl {
  public:

    explicit DoubleArrayImpl(): array_(0), used_(0),
                                size_(0), alloc_size_(0),
                                no_delete_(0), error_(0);
    ~DoubleArrayImpl();


    void clear();
    size_t unit_size();
    size_t size();
    size_t total_size() const;

    size_t nonzero_size() const;

    int build(size_t key_size, char **key,
              size_t     *length = 0,
              value_type *value = 0,
              int (*progress_func)(size_t, size_t) = 0);

    int save(const char *file,
             const char *mode = "wb",
             size_t offset = 0);

    template <class T>
    inline void exactMatchSearch(const key_type *key,
                                 T & result,
                                 size_t len = 0,
                                 size_t node_pos = 0);

    template <class T>
    inline T exactMatchSearch(const key_type *key,
                              size_t len = 0,
                              size_t node_pos = 0);
    template <class T>
    size_t commonPrefixSearch(const key_type *key,
                              T* result,
                              size_t result_len,
                              size_t len = 0,
                              size_t node_pos = 0);

    value_type traverse(const key_type *key,
                        size_t &node_pos,
                        size_t &key_pos,
                        size_t len = 0);
  };

}

%template(DoubleArray) Darts::DoubleArrayImpl<char, unsigned char, int, unsigned int> ;