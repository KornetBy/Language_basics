#include <iostream>
#include <string>

using namespace std;

class Building {
public:
	
	int year;
	string type;

	void get_info() {
		cout << "Type: " << type << "; Year: " << year << endl;
	}

};


int main() {
	setlocale(LC_ALL, "RU");

	Building school;
	school.type = "Ўкола";
	school.year = 2000;
	school.get_info();



	return 0;
}