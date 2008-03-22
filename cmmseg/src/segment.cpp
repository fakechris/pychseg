// TODO: add license here --> Chris Song

#include "conf.h"
#include "dict.h"
#include "utf8.h"
#include "segment.h"

inline int DataLoader::check_bom_header(const uint8_t* buf) {
    if ( HAS_NEXT_3CHAR(buf) ) {
        uint8_t c = *buf;
        if (c == 0x0 || c == 0xff || c == 0xfe) {
            return ERROR_EMPTY_STRING_OR_NOTUTF8_FILE;
        }
        // if is utf8 BOM header, skip it
        if (c == 0xef) {
            ASSERT( *(buf+1) == 0xbb );
            ASSERT( *(buf+2) == 0xbf );            
            _pos += 3;
        }
    }        
    return ERROR_NONE;
}

int DataLoader::next_fragment() {
    int ret;
    
    // start of stream, check start of BOM
    if ( _pos == NULL ) {
        _pos = input_;
        ret = check_bom_header();
        if (ret != ERROR_NONE)
            return ret;
    }
    
    // parse utf8 stream into fragments (chinese, english, stop word or other token)
    
    
    return ret;
}

int StreamLoader::next_fragment() {
    int ret;
    
    // alloca memory, 64k as a batch
    input_ = new unint8_t[65536];
    
    // read max 64k data from stream_
    stream_ >> intput_;
    // then find utf8 fragment
    
    
    //DataLoader::next_fragment();
    
    
    // parse utf8 stream into fragments (chinese, english, stop word or other token)
    
    return ret;
}


/*
int StreamLoader::check_bom_header() {
    uint8_t c = stream_.peek();
    if (c == 0x0 || c == 0xff || c == 0xfe) {
        return ERROR_EMPTY_STRING_OR_NOTUTF8_FILE;
    }
    // if is utf8 BOM header, skip it
    if (c == 0xef) {
        stream_ >> c;
        ASSERT( c == 0xef );
        ASSERT( stream_ );
        stream_ >> c;
        ASSERT( c == 0xbb );
        ASSERT( stream_ );
        stream_ >> c;
        ASSERT( c == 0xbf );
        ASSERT( stream_ );
    }
    return ERROR_NONE;
}

int StreamLoader::next_fragment() {
    uint8_t c = 0xff;
    int ret;
    // start of stream, check start of BOM
    if ( (int)stream_.tellg() == 0 ) {
        ret = check_bom_header();
        if (ret != ERROR_NONE)
            return ret;
    }
    // parse utf8 stream into fragments (chinese, english, stop word or other token)
    while(stream_) {
        stream_ >> c;
        // check if 
    }
    return ret;
}
*/

void BaseSegment::feed_input(uint8_t * input, int len) {
    input_ = input;
    len_ = len;
}

int FMMSegment::next_token(uint8_t *& buf, int& len) {
    return 1;
}

int FMMSegment::next_token(uint8_t * buf) {
    return 1;
}


int ComplexMMgSegment::next_token(uint8_t *& buf, int& len) {
    return 1;
}

int ComplexMMgSegment::next_token(uint8_t * buf) {
    return 1;
}
