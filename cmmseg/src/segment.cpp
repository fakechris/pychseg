// TODO: add license here --> Chris Song

#include "conf.h"
#include "dict.h"
#include "utf8.h"
#include "segment.h"

int StreamLoader::check_bom_header() {
	unsigned char c = stream_.peek();
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
	unsigned char c = 0xff;
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

void BaseSegment::feed_input(unsigned char * input, int len) {
	input_ = input;
	len_ = len;
}

int FMMSegment::next_token(unsigned char *& buf, int& len) {
	return 1;
}

int FMMSegment::next_token(unsigned char * buf) {
	return 1;
}


int ComplexMMgSegment::next_token(unsigned char *& buf, int& len) {
	return 1;
}

int ComplexMMgSegment::next_token(unsigned char * buf) {
	return 1;
}
