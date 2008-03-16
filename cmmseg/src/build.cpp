
#include <iostream>
#include <fstream>
using namespace std;

#include "darts.h"
using namespace Darts;

int main(int argc, char* argv[])
{

	ifstream in("../dict/words.lex");                 // input

	if(!in) {
		cout << "Cannot open input file.\n";
		return 1;
	}

	char ** buf = new char*[655350];
	int i=0;
	while(in) {
		char * str = new char[64];
		in.getline(str, 64);                // delim defaults to '\n'
		//if(in) 
		//	cout << str << endl;
		buf[i] = str;
		i++;
		if (i % 100 == 0)
			cout << i << str << endl;
	}

	in.close();

	DoubleArray* da = new DoubleArray();
	da->build(i, (char**)buf);

	da->save("../dict/dartswords.lex");

	return 0;
}