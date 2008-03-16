
/**
  * TODO: add license here --> Chris Song
  */

#ifndef _CMMSEG_CHUNK_H_
#define _CMMSEG_CHUNK_H_

#include <math.h>

template <class T> inline void takeHighest(T* list, int len, T* result, int (*compar)(const void *, const void *)) {
	for (int i = 0; i < len; i++) {
		compar(NULL, NULL); 
	}
}

typedef struct _Word {
	//unsigned char * start;
	//unsigned char * end;
	int wordLen; // utf8 word len, not end-start
	double freq; // if wordLen == 1
} Word;

class Chunk {
private:
	Word * words;
	int len;
	
	// caching type 1 --> per Chunk cache
	int cacheLength;
	double cacheAverageLength;
	double cacheVariance;
	double cacheDegree;
	unsigned int cacheReverseLength;

	// TODO: caching type 2 --> per WordList cache
public:	
	Chunk(Word* words, int len) : cacheLength(0), cacheAverageLength(-1.0), cacheVariance(-1.0), cacheDegree(-1.0), cacheReverseLength(0) {
		this->words = words;
		this->len = len;		
	}
	
	int length() {
		if (cacheLength != 0) 
			return cacheLength;

		for (int i = 0; i < len; i++) 
			cacheLength += words[i].wordLen;
		return cacheLength;
	}
	
	double averageLength() {
		if (cacheAverageLength > 0.0) 
			return cacheAverageLength;
		
		cacheAverageLength = double(length()) / len;
		return cacheAverageLength;
	}
	
	double variance() {
		if (cacheVariance > -1.0) 
			return cacheVariance;
		
		double average = averageLength();
		cacheVariance = 0.0;
		for (int i = 0; i < len; i++)
			cacheVariance += pow(words[i].wordLen-average, 2) ;
		cacheVariance = sqrt( cacheVariance/len	);
		return cacheVariance;
	}
	
	double degreeOfMorphemicFreedom() {
		if (cacheDegree > -1.0)
			return cacheDegree;
		
		cacheDegree = 0.0;
		for (int i = 0; i < len; i++)
			if (words[i].freq > 1.0)
				cacheDegree += log(words[i].freq);
		return cacheDegree;
	}
	
	int reverseLength() {
		if (cacheReverseLength != 0)
			return cacheReverseLength;
			
		for (int i = 0; i < len; i++)
			cacheReverseLength += words[i].wordLen << (i<<3);
		return cacheReverseLength;
	}
};

#endif