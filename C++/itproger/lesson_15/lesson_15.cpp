#include <iostream>
#include <string>

using namespace std;

enum Options {
	open = 4, 
	close,
	wait,
	del

 };
struct File {
	int weight;
	string name;
	Options options;
};

int main() {
	setlocale(LC_ALL, "RU");
	
	File my_file;
	my_file.weight = 1;
	my_file.name = "test.txt";
	my_file.options = Options::open;
	if (my_file.options == Options::close)
		cout << "File is close" << endl;
	else
		cout << "Smth else";
	
	return 0;
}