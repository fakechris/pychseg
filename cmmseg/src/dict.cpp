
#include <stdio.h>

#include <iostream>
#include <fstream>
#include <memory>
#include <list>
using namespace std;

#include "dict.h"

WordDict* WordDict::_instance;
WordDict* WordDict::Instance(){
    if( _instance == 0){
        _instance = new WordDict;
		_instance->load();
    };
    return _instance;
}

WordDict::WordDict() : doubleArray(NULL) {	
}

int WordDict::load() {
	doubleArray = new DoubleArray();

	ifstream in("../dict/words.lex"); 
	if(!in) {
		return -1;
	}

	//TODO: assume dict contains 200k entries max
	auto_ptr<char *> buf(new char*[204800]);	
	auto_ptr<char *> words((char**)new char[204800][64]);

	int i=0;
	while(in) {
		//TODO: assume max word len 20
		//char * str = (char*)words+64*i;
		char * str = (char*)words.get()+64*i;
		in.getline(str, 64);		
		buf.get()[i] = str;		
		i++;	
	}
	in.close();

	doubleArray->build(i, (char**)(buf.get()));

	return 1;
}

int WordDict::exactMatchSearch(const char *key, size_t len, size_t node_pos) {
	int result;
	doubleArray->exactMatchSearch(key, result, len, node_pos);
	return result;
}

size_t WordDict::commonPrefixSearch(const char *key,
                              int* result,
                              size_t result_len,
                              size_t len,
							  size_t node_pos) {
	return doubleArray->commonPrefixSearch(key, result, result_len, len, node_pos);
}


CharDict* CharDict::_instance;
CharDict* CharDict::Instance(){
    if( _instance == 0){
        _instance = new CharDict;
		_instance->load();
    };
    return _instance;
}

CharDict::CharDict() : utf8charfreq(NULL) {
	
}

int CharDict::load() {
	utf8charfreq = new Utf8CharFreq();

	ifstream in("../dict/chars.lex"); 
	if(!in) {
		return -1;
	}

	unsigned char str[64];
	unsigned char utf8char[4];
	unsigned int freq;
	while(in) {
		in.getline((char*)str, 64);		
		sscanf_s((const char*)str, "%4s %lu", utf8char, 4, &freq);
		utf8charfreq->set(utf8char, freq);
	}
	in.close();	

	return 0;
}

unsigned int CharDict::get(unsigned char * utf8c) {
	return utf8charfreq->get(utf8c);
}