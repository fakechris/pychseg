// TODO: add license here --> Chris Song

#ifndef _CMMSEG_SEGMENT_H_
#define _CMMSEG_SEGMENT_H_

#include <iostream>

#define ERROR_NONE 0
#define ERROR_EMPTY_STRING_OR_NOTUTF8_FILE -1

class Segment {
public:
	virtual void feed_input(unsigned char * input, int len) = 0;
	// return a temp buffer
	virtual int next_token(unsigned char *& buf, int& len) = 0;
	// caller should provide buf
	virtual int next_token(unsigned char * buf) = 0;
};

class StreamLoader {
private:
	std::istream& stream_;
	int check_bom_header();
public:
	StreamLoader(std::istream& stream) : stream_(stream) {}
	int next_fragment();
};

class BaseSegment : Segment {
private:
	unsigned char* input_;
	int len_;
public:
	virtual void feed_input(unsigned char * input, int len);
};

class FMMSegment : BaseSegment {
public:
	
	virtual int next_token(unsigned char *& buf, int& len);
	virtual int next_token(unsigned char * buf);
};

class ComplexMMgSegment : BaseSegment {
public:
	virtual int next_token(unsigned char *& buf, int& len);
	virtual int next_token(unsigned char * buf);
};

#endif