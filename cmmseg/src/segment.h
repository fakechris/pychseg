// TODO: add license here --> Chris Song

#ifndef _CMMSEG_SEGMENT_H_
#define _CMMSEG_SEGMENT_H_

#include <iostream>

#define ERROR_NONE 0
#define ERROR_EMPTY_STRING_OR_NOTUTF8_FILE -1

/*
class StreamLoader {
private:
    std::istream& stream_;
    int check_bom_header();
public:
    StreamLoader(std::istream& stream) : stream_(stream) {}
    int next_fragment();
};
*/

class DataLoader {
private:
    const char* input_;
    const char* pos_;
    int check_bom_header(const uint8_t* buf);
public:
    DataLoader(const char* input) : input_(input), pos_(NULL) {}
    virtual int next_fragment();
};

class StreamLoader : DataLoader {
private:
    std::istream& stream_;
public:
    StreamLoader(std::istream* stream) : stream_(stream), input_(NULL), pos_(NULL) {}
    virtual int next_fragment();
}

class Segment {
public:
    virtual void feed_input(uint8_t * input, int len) = 0;
    // return a temp buffer
    virtual int next_token(uint8_t *& buf, int& len) = 0;
    // caller should provide buf
    virtual int next_token(uint8_t * buf) = 0;
};

class BaseSegment : Segment {
private:
    uint8_t* input_;
    int len_;
public:
    virtual void feed_input(uint8_t * input, int len);
};

class FMMSegment : BaseSegment {
public:
    
    virtual int next_token(uint8_t *& buf, int& len);
    virtual int next_token(uint8_t * buf);
};

class ComplexMMgSegment : BaseSegment {
public:
    virtual int next_token(uint8_t *& buf, int& len);
    virtual int next_token(uint8_t * buf);
};

#endif