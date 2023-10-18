#include <iostream>
#include <string>

using namespace std;

class Building {
private:
	int year;
	string type;

public:
	Building(int y) {
		year = y;
	}

	Building(int year, string type) {
		this->year = year;
		this->type = type;

	}


	void set_data(int y, string t) {
		year = y;
		type = t;
	}

	void get_info() {
		cout << "Type: " << type << "; Year: " << year << endl;
	}
	~Building() {
		cout << "Delete object" << endl;
	}
};


int main() {
	setlocale(LC_ALL, "RU");

	Building school(2000, "Ўкола");
	school.get_info();



	return 0;
}