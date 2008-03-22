// TODO: add license here --> Chris Song

#ifndef _CMMSEG_UTF8_H_
#define _CMMSEG_UTF8_H_

#include "conf.h"

/*!
    \param src   begin pointer of string
    \param end   end pointer of string
    \return   1,2,3 next utf8 word length, 0 reach string end or not valid end, -1 invalid utf8 char, skip it.
inline int next_utf8_word(uint8_t* src, uint8_t* end) { 
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
*/

inline int next_utf8_word(uint8_t* src) { 
    if (*src == 0) // not a word
        return 0;
    if (((*src) & 0x80) == 0) {
        return 1;
    } else if (((*src) & 0xe0) == 0xc0) {
        if (*(src+1) == 0) // not valid utf8 word, maybe lost bytes
            return 0;
        return 2;
    } else if (((*src) & 0xf0) == 0xe0) {
        if (*(src+2)==0 || *(src+1)==0) // not valid utf8 word, maybe lost bytes
            return 0;
        return 3;
    }
    //utf8 should NEVER reach here
    return -1;
}

inline int is_latin(uint8_t c) {
    return ( (c&0x80) == 0 );
}

// TODO: check utf8 char type, alpha, digit, tokens, spaces, crlf
//     skip              crlf
//     break             tokens, spaces
//     breakbetween      alpha/digit cjk word

inline int is_space(uint8_t c) {
    /* 0x20 */
    return 1;
}

inline int is_crlf(uint8_t c) {
}

inline int is_token(uint8_t c) {
    /* 0x21-0x2f 0x3a-0x40 0x5b-0x60 0x7b-0x7e */
}

inline int is_alpha(uint8_t c) {
    /* 0x41-0x5a 0x61-0x7a */
}

inline int is_digit(uint8_t c) {
    /* 0x30-0x39 */
}

inline int is_cjk(uint8_t c) {
} 

/*
utf16 code page
0x80-0xbf 0xd7 0xf7 token
0xc0-0xd6 0xd8-0xf6 0xf8-0xff 0x100-0x17f 0x180-0x24f 0x250-0x2af latin
0x370-0x3ff greek
0x400-0x4ff 0x500-0x52f cyrillic
0x530-0x58f armenian
0x590-0x5ff hebrew
0x600-0x6ff 0x750-0x77f arabic
0x700-0x74f syriac
0x780-0x7bf thaana
0x900-0x97f devanagari
0x980-0x9ff bengali
0xa00-0xa7f gurmukhi
0xa80-0xaff gujarati
0xb00-0xb7f oriya
0xb80-0xbff tamil
0xc00-0xc7f telugu
0xc80-0xcff kannada
0xd00-0xd7f malayalam
0xd80-0xdff sinhala
0xe00-0xe7f thai
0xe80-0xeff lao
0xf00-0xfff tibetan

0x20a0-0x20cf currency symbols (***)
0x2150-0x218f number forms
0x2200-0x22ff math operators
0x2460-0x24ff enclosed letters
0x2500-0x26ff symbols

0x2e80-0x2eff cjk radicals supplement
0x3000-0x303f cjk symbols (tokens)
0x3200-0x32ff enclosed cjk letters/months
0x3300-0x33ff cjk compatibility

0x1100-0x11ff Hangul Jamo (korea)
0xac00-0xd7a3 Hangul Syllables (korea)
0x3130-0x318f Hangul Compatibility Jamo (korea)

0x3040-0x309f Hiragana (japan)
0x30a0-0x30ff Katakana (japan)
0x3190-0x319f Kanbun (japan old chinese)

0x3100-0x312f Bomomofo (old chinese pinyin)
0x4e00-0x9fbb 0xf9ff-0xfaff CJK unified ideographs (chinese goes here)

0xa000-0xa4cf Yi Syllables (south-east chinese)

*/

// convert between SBC(quanjiao) <-> DBC(banjiao), utf16
inline uint16_t utf16_dbc2sbc(uint16_t c)
{
    if (c == 32)
        return  12288;
    if (c < 127)
        return c + 65248;
    return c;
}

inline uint16_t utf16_sbc2dbc(uint16_t c)
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
    uint32_t utf8Matrix[6][64][64];     
    // a trick maybe has potential danger
    // for boost performance -> adjust start pos of utf8Matrix, minus 0xe4*64*64*4 --> '0x390000'
    uint32_t * utf8MatrixVirtualStart;
public:
    Utf8CharFreq() {
        memset((void*)utf8Matrix, 0, sizeof(utf8Matrix));
        ASSERT((uint32_t)(void*)utf8Matrix > 0x390000);
        utf8MatrixVirtualStart = (uint32_t *)((char*)utf8Matrix - 0xe4*64*64*sizeof(uint32_t));     
    }
    void set(uint8_t * utf8c, uint32_t freq) {
        //ASSERT (! (*utf8c > 0xe9 || *utf8c  0xe4 || *(utf8c+1) > 0xbf || *(utf8c+1) < 0x80 || *(utf8c+2) > 0xbf || *(utf8c+2) < 0x80) );
        if (*utf8c > 0xe9 || *utf8c < 0xe4 || *(utf8c+1) > 0xbf || *(utf8c+1) < 0x80 || *(utf8c+2) > 0xbf || *(utf8c+2) < 0x80)
            return;
        *(utf8MatrixVirtualStart + (*utf8c << 12) + ((*(utf8c+1) & 0x7f) << 6) + (*(utf8c+2) & 0x7f)) = freq;
    }
    uint32_t get(uint8_t * utf8c) {
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
    uint32_t utf8Matrix[6][64][64];     
public:
    Utf8CharFreq() {
        memset((void*)utf8Matrix, 0, sizeof(utf8Matrix));
    }
    void set(uint8_t * utf8c, uint32_t freq) {
        utf8Matrix[*utf8c-0xer][*(utf8c+1) & 0x7f][*(utf8c+2) & 0x7f] = freq;
    }
    uint32_t get(uint8_t * utf8c) {
        if (*utf8c > 0xe9 || *utf8c < 0xe4 || *(utf8c+1) > 0xbf || *(utf8c+1) < 0x80 || *(utf8c+2) > 0xbf || *(utf8c+2) < 0x80)
            return 0;       
        return utf8Matrix[*utf8c-0xer][*(utf8c+1) & 0x7f][*(utf8c+2) & 0x7f];
    }
};

class Utf8CharFreqUncompress {
private:
    uint32_t utf8Matrix[6][256][256];
    uint32_t *** utf8MatrixVirtualStart;
public:
    Utf8CharFreq() {
        memset(utf8Matrix, sizeof(utf8Matrix), 0);
        utf8MatrixVirtualStart = (uint32_t ***)((void*)utf8Matrix - 0xe4*256*256*sizeof(uint32_t))
    }
    void set(uint8_t * utf8c, uint32_t freq) {
        utf8MatrixVirtualStart[*utf8c][*(utf8c+1)][*(utf8c+2)] = freq;
    }
    uint32_t get(uint8_t * utf8c) {
        return utf8MatrixVirtualStart[*utf8c][*(utf8c+1)][*(utf8c+2)];
    }
};
*/

#endif