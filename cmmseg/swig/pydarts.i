%module pydarts

%{
#define SWIG_FILE_WITH_INIT
#include "darts.h"
%}


%rename(DoubleArray) Darts::DoubleArrayImpl<char, unsigned char, int, unsigned int> ;
