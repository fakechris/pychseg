#include <cxxtest/TestSuite.h>

#include "../src/utf8.h"
#include "../src/chunk.h"

class CmmsegTestSuite : public CxxTest::TestSuite 
{
public:

	void testUtf8CharFreq( void )
	{
		unsigned char c1[3] = {0xe4, 0x80, 0x80};
		unsigned char c2[3] = {0xe5, 0xb0, 0x97};
		unsigned char c3[3] = {0xe9, 0xbf, 0xbf};
		unsigned char c4[3] = {0xa0, 0x80, 0xbf};
		unsigned char c5[3] = {0xe5, 0x32, 0xbf};
		unsigned char c6[3] = {0xe5, 0x80, 0xff};
		/*
		Utf8CharFreq utf8charfreq;
		utf8charfreq.set(c1, 123);
		utf8charfreq.set(c2, 22123);
		utf8charfreq.set(c3, 13123);
		
		TS_ASSERT_EQUALS( utf8charfreq.get(c1), 123 );
		TS_ASSERT_EQUALS( utf8charfreq.get(c2), 22123 );
		TS_ASSERT_EQUALS( utf8charfreq.get(c3), 13123 );
		
		TS_ASSERT_EQUALS( utf8charfreq.get(c1), 0 );
		TS_ASSERT_EQUALS( utf8charfreq.get(c2), 0 );
		TS_ASSERT_EQUALS( utf8charfreq.get(c3), 0 );
		*/
		Utf8CharFreq * utf8charfreq = new Utf8CharFreq();
		utf8charfreq->set(c1, 123);
		utf8charfreq->set(c2, 22123);
		utf8charfreq->set(c3, 13123);
		
		TS_ASSERT_EQUALS( utf8charfreq->get(c1), 123 );
		TS_ASSERT_EQUALS( utf8charfreq->get(c2), 22123 );
		TS_ASSERT_EQUALS( utf8charfreq->get(c3), 13123 );
		
		TS_ASSERT_EQUALS( utf8charfreq->get(c4), 0 );
		TS_ASSERT_EQUALS( utf8charfreq->get(c5), 0 );
		TS_ASSERT_EQUALS( utf8charfreq->get(c6), 0 );
		
	}

	void testChunk( void )
	{
		Word w1[3] = { {2,0}, {2,0}, {2,0} };
		Chunk c1((Word*)w1,3);
		TS_ASSERT_EQUALS( c1.length(), 6 );
		TS_ASSERT_EQUALS( c1.averageLength(), 2.0 );
		TS_ASSERT_EQUALS( c1.variance(), 0.0 );
		
		Word w2[3] = { {3,0}, {1,0}, {2,0} };
		Chunk c2((Word*)w2,3);
		TS_ASSERT_EQUALS( c2.length(), 6 );
		TS_ASSERT_EQUALS( c2.averageLength(), 2.0 );
		TS_ASSERT_EQUALS( c2.variance(), 0.81649658092772603 );
		
		Word w3[3] = { {2,0}, {1,3200626}, {2,0} };
		Chunk c3((Word*)w3,3);
		TS_ASSERT_EQUALS( c3.degreeOfMorphemicFreedom(), 14.97885697363788 );
		TS_ASSERT_EQUALS( c3.reverseLength(), 131330 );
		
	}
};
