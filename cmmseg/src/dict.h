#ifndef _CMMSEG_DICT_H_
#define _CMMSEG_DICT_H_

#include "darts.h"
using namespace Darts;
#include "utf8.h"

class WordDict{
public:
    static WordDict* Instance();	
    int exactMatchSearch(const char *key, size_t len = 0, size_t node_pos = 0);	
    size_t commonPrefixSearch(const char *key,
                              int* result,
                              size_t result_len,
                              size_t len = 0,
                              size_t node_pos = 0);
protected:
	WordDict();
private:
	DoubleArray* doubleArray;
    static WordDict* _instance;

	int load();
};

class CharDict{
public:
    static CharDict* Instance();
	unsigned int get(unsigned char * utf8c);
protected:
    CharDict();
private:
	Utf8CharFreq * utf8charfreq;
    static CharDict* _instance;

	int load();
};

#endif