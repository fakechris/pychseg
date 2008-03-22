// TODO: add license here --> Chris Song

#ifndef _CMMSEG_CONF_H_
#define _CMMSEG_CONF_H_

#include <assert.h>

#define ASSERT(x) assert(x)
#define LOG(x)  

#ifndef uint8_t
#define uint8_t unsigned char
#endif
#ifndef uint16_t
#define uint16_t unsigned short
#endif
#ifndef uint32_t
#define uint32_t unsigned int
#endif
#ifndef uint64_t
#define uint64_t unsigned long /*long*/
#endif

#define HAS_NEXT_CHAR(s) ( *s!=0 )
#define HAS_NEXT_2CHAR(s) ( *s!=0 && *(s+1)!=0 )
#define HAS_NEXT_3CHAR(s) ( *s!=0 && *(s+1)!=0 && *(s+2)!=0 )

#endif