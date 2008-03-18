// TODO: add license here --> Chris Song
// wordtest.cpp : Defines the entry point for the console application.
//

#include <iostream>
#include <tchar.h>

#include "darts.h"
using namespace Darts;

#include "dict.h"

#include <strstream>

int _tmain(int argc, _TCHAR* argv[])
{

	std::istrstream is("test");
	unsigned char cc;
	int pos;
	pos = is.tellg();
	while(is)
		is >> cc;
	pos = is.tellg();

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

	WordDict * w = WordDict::Instance();
	CharDict * c = CharDict::Instance();

	unsigned char c1[3] = {0xe7, 0x9a, 0x84};
	unsigned int r = c->get(c1);

	//unsigned char c2[13] = {0xe4, 0xb8, 0x80, 0xe4, 0xb8, 0x96, 0xe4, 0xb9, 0x8b, 0xe9, 0x9b, 0x84, 0x0};
	unsigned char c2[7] = {0xe4, 0xb8, 0x80, 0xe4, 0xb8, 0x80, 0x0};
	int r2 = w->exactMatchSearch((const char*)c2);

	std::cout << r << " " << r2;

	return 0;
}

