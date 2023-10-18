#include <iostream>
#include <string>
#include <fstream>
using namespace std;


int main() {
	setlocale(LC_ALL, "RU");
	
	/*ofstream file("test.txt", ios_base::out);

	if (file.is_open()) {
		file << "HELLO WORLD";
		file.close();
	}*/

	ifstream file("test.txt");
	
	if (file.is_open()) {
		
		//string temp;
		//file >> temp;
		char temp[100];
		file.getline(temp, 100);
		cout << temp << endl;
		file.close();
	}


	return 0;
}