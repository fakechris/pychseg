
/**
  * TODO: add license here --> Chris Song
  */

#ifndef _CMMSEG_UTF8_H_
#define _CMMSEG_UTF8_H_

/*!
	\param src   begin pointer of string
	\param end   end pointer of string
    \return   1,2,3 next utf8 word length, 0 reach string end or not valid end, -1 invalid utf8 char, skip it.
*/
inline int next_utf8_word(unsigned char* src, unsigned char* end) { 
	if (end <= src) // not a word
		return 0;
	if (((*src) & 0x80) == 0) {
		return 1;
	} else if (((*src) & 0xe0) == 0xc0) {
		if (end < src+1) // not valid utf8 word, maybe lost bytes
			return 0;
		return 2;
	} else if (((*src) & 0xf0) == 0xe0) {
		if (end < src+2) // not valid utf8 word, maybe lost bytes
			return 0;
		return 3;
	}
	//utf8 should NEVER reach here
	return -1;
}

inline int is_latin(unsigned char c) {
	return ( (c&0x80) == 0 );
}

// convert between SBC(quanjiao) <-> DBC(banjiao), utf16
inline unsigned short utf16_dbc2sbc(unsigned short c)
{
	if (c == 32)
		return  12288;
	if (c < 127)
		return c + 65248;
	return c;
}

inline unsigned short utf16_sbc2dbc(unsigned short c)
{
	if (c == 12288)
		return 32;
	if (c > 65280 && c < 65375)
		return c - 65248;
    return c;
}


/**
 * optimized version
 * WARNNING: this class MUST BE ALLOCATED ON HEAP, NOT STACK, because utf8Matrix's address should located after 0x390000 
 */
class Utf8CharFreq {
private:
	// utf8Matrix to save chinese char freq	
	// 0xe9 - 0xe4, 0xbf - 0x80, 0xbf - 0x80
	// a - 0x08 --> a & 0x7f
	unsigned int utf8Matrix[6][64][64];		
	// a trick maybe has potential danger
	// for boost performance -> adjust start pos of utf8Matrix, minus 0xe4*64*64*4 --> '0x390000'
	unsigned int * utf8MatrixVirtualStart;
public:
	Utf8CharFreq() {
		memset((void*)utf8Matrix, 0, sizeof(utf8Matrix));
		utf8MatrixVirtualStart = (unsigned int *)((char*)utf8Matrix - 0xe4*64*64*sizeof(unsigned int));		
	}
	void set(unsigned char * utf8c, unsigned int freq) {
		//assert (! (*utf8c > 0xe9 || *utf8c  0xe4 || *(utf8c+1) > 0xbf || *(utf8c+1) < 0x80 || *(utf8c+2) > 0xbf || *(utf8c+2) < 0x80) );
		*(utf8MatrixVirtualStart + (*utf8c << 12) + ((*(utf8c+1) & 0x7f) << 6) + (*(utf8c+2) & 0x7f)) = freq;
	}
	unsigned int get(unsigned char * utf8c) {
		if (*utf8c > 0xe9 || *utf8c < 0xe4 || *(utf8c+1) > 0xbf || *(utf8c+1) < 0x80 || *(utf8c+2) > 0xbf || *(utf8c+2) < 0x80)
			return 0;		
		return *(utf8MatrixVirtualStart + (*utf8c << 12) + ((*(utf8c+1) & 0x7f) << 6) + (*(utf8c+2) & 0x7f));
	}
};

/*
class Utf8CharFreq {
private:
	// utf8Matrix to save chinese char freq	
	// 0xe9 - 0xe4, 0xbf - 0x80, 0xbf - 0x80
	// a - 0x08 --> a & 0x7f
	unsigned int utf8Matrix[6][64][64];		
public:
	Utf8CharFreq() {
		memset((void*)utf8Matrix, 0, sizeof(utf8Matrix));
	}
	void set(unsigned char * utf8c, unsigned int freq) {
		utf8Matrix[*utf8c-0xer][*(utf8c+1) & 0x7f][*(utf8c+2) & 0x7f] = freq;
	}
	unsigned int get(unsigned char * utf8c) {
		if (*utf8c > 0xe9 || *utf8c < 0xe4 || *(utf8c+1) > 0xbf || *(utf8c+1) < 0x80 || *(utf8c+2) > 0xbf || *(utf8c+2) < 0x80)
			return 0;		
		return utf8Matrix[*utf8c-0xer][*(utf8c+1) & 0x7f][*(utf8c+2) & 0x7f];
	}
};

class Utf8CharFreqUncompress {
private:
	unsigned int utf8Matrix[6][256][256];
	unsigned int *** utf8MatrixVirtualStart;
public:
	Utf8CharFreq() {
		memset(utf8Matrix, sizeof(utf8Matrix), 0);
		utf8MatrixVirtualStart = (unsigned int ***)((void*)utf8Matrix - 0xe4*256*256*sizeof(unsigned int))
	}
	void set(unsigned char * utf8c, unsigned int freq) {
		utf8MatrixVirtualStart[*utf8c][*(utf8c+1)][*(utf8c+2)] = freq;
	}
	unsigned int get(unsigned char * utf8c) {
		return utf8MatrixVirtualStart[*utf8c][*(utf8c+1)][*(utf8c+2)];
	}
};
*/

#endif