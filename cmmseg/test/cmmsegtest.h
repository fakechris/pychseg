#include <cxxtest/TestSuite.h>
 
class CmmsegTestSuite : public CxxTest::TestSuite 
{
public:
	void testAddition( void )
	{
		TS_ASSERT( 1 + 1 > 1 );
		TS_ASSERT_EQUALS( 1 + 1, 2 );
	}

	void testMultiplication( void )
	{
		TS_ASSERT_EQUALS( 2 * 2, 5 );
	}
};
