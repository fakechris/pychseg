#include <cxxtest/TestSuite.h>

#include "../src/utf8.h"

class CmmsegTestSuite : public CxxTest::TestSuite 
{
public:

	void testUtf8CharFreq( void )
	{
		unsigned char c1[3] = {0xe4, 0x80, 0x80};
		unsigned char c2[3] = {0xe5, 0xb0, 0x97};
		unsigned char c3[3] = {0xe9, 0xbf, 0xbf};
		Utf8CharFreq utf8charfreq;
		utf8charfreq.set(c1, 123);
		utf8charfreq.set(c2, 22123);
		utf8charfreq.set(c3, 13123);
		
		TS_ASSERT_EQUALS( utf8charfreq.get(c1), 123 );
		TS_ASSERT_EQUALS( utf8charfreq.get(c2), 22123 );
		TS_ASSERT_EQUALS( utf8charfreq.get(c3), 13123 );
	}

	void testMultiplication( void )
	{
		TS_ASSERT_EQUALS( 2 * 2, 5 );
	}
};
