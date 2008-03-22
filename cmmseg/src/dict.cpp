// TODO: add license here --> Chris Song

#include <stdio.h>

#include <iostream>
#include <fstream>
#include <memory>
#include <list>
using namespace std;

#include "conf.h"
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

//TODO: assume dict contains 200k entries max
#define MAX_WORDDICT_LEN 204800
#define MAX_WORD_LEN 64
int WordDict::load() {
    doubleArray = new DoubleArray();

    ifstream in("../dict/words.lex"); 
    if(!in) {
        return -1;
    }
    
    auto_ptr<char *> buf(new char*[MAX_WORDDICT_LEN]);  
    auto_ptr<char *> words((char**)new char[MAX_WORDDICT_LEN][MAX_WORD_LEN]);

    int i=0;
    while(in) {
        char * str = (char*)words.get()+MAX_WORD_LEN*i;
        in.getline(str, MAX_WORD_LEN);  
        if (str[0] != 0) {
            buf.get()[i] = str;     
            i++;
            ASSERT( i < MAX_WORDDICT_LEN );
        }
    }
    in.close();

    doubleArray->build(i, (char**)(buf.get()));

    return 1;
}

int WordDict::exactMatchSearch(const uint8_t *key, size_t len, size_t node_pos) {
    int result;
    doubleArray->exactMatchSearch(key, result, len, node_pos);
    return result;
}

size_t WordDict::commonPrefixSearch(const uint8_t *key,
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

#define MAX_WORDFREQ_LEN 64
int CharDict::load() {
    utf8charfreq = new Utf8CharFreq();

    ifstream in("../dict/chars.lex"); 
    if(!in) {
        return -1;
    }

    uint8_t str[MAX_WORDFREQ_LEN];
    uint8_t utf8char[4];
    unsigned int freq;
    while(in) {
        in.getline((char*)str, MAX_WORDFREQ_LEN);       
        sscanf_s((const char*)str, "%4s %lu", utf8char, 4, &freq);
        utf8charfreq->set(utf8char, freq);
    }
    in.close(); 

    return 0;
}

unsigned int CharDict::get(uint8_t * utf8c) {
    return utf8charfreq->get(utf8c);
}