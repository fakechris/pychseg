// wordtest.cpp : Defines the entry point for the console application.
//

#include "darts.h"

#include <tchar.h>

using namespace Darts;

int _tmain(int argc, _TCHAR* argv[])
{
	/* simple test method */
	DoubleArray* da = new DoubleArray();

	const char * buf[] = {"test", "tf", "tfcc", "zl"};

	da->build(4, (char**)buf);


	int result;

	da->exactMatchSearch("test", result);	
	printf("%d\n", result);
	da->exactMatchSearch("tfcc", result);
	printf("%d\n", result);	
	da->exactMatchSearch("zl", result);
	printf("%d\n", result);

	da->exactMatchSearch("testsdf", result);	
	printf("%d\n", result);
	da->exactMatchSearch("tfcs", result);
	printf("%d\n", result);	
	da->exactMatchSearch("sdzl", result);
	printf("%d\n", result);

	int results[20];
	int resultlen = sizeof(results);
	int ret;
	ret = da->commonPrefixSearch("test", results, resultlen);	
	printf("%d %d\n", results[0], ret);
	ret = da->commonPrefixSearch("tfcc", results, resultlen);
	printf("%d %d\n", results[0], ret);
	ret = da->commonPrefixSearch("zl", results, resultlen);
	printf("%d %d\n", results[0], ret);

	ret = da->commonPrefixSearch("testsdf", results, resultlen);	
	printf("%d %d\n", results[0], ret);
	ret = da->commonPrefixSearch("tfcsc", results, resultlen);
	printf("%d %d\n", results[0], ret);
	ret = da->commonPrefixSearch("sdzl", results, resultlen);
	printf("%d %d\n", results[0], ret);

	

	return 0;
}

