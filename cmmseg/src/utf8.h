
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


class Utf8CharFreq {
private:
	// utf8Matrix to save chinese char freq
	// 0xe9 - 0xe4, 0xbf - 0x80, 0xbf - 0x80
	unsigned int utf8Matrix[6][64][64];
public:
	Utf8CharFreq() {
		memset(utf8Matrix, sizeof(utf8Matrix), 0);
	}
	void set(unsigned char * utf8c, unsigned int freq) {
		utf8Matrix[*utf8c-0xe4][*(utf8c+1)-0x80][*(utf8c+2)-0x80] = freq;
	}
	unsigned int get(unsigned char * utf8c) {
		return utf8Matrix[*utf8c-0xe4][*(utf8c+1)-0x80][*(utf8c+2)-0x80];
	}
};

#endif