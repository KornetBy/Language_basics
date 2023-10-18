#include <iostream>
#include <string>

using namespace std;


struct Tree {
	string name;
	int ages;
	bool is_alive;
	float height;
	void get_all_info() {
		cout << "Name: " << name;
		cout << "Ages: " << ages;
	}
};

int main() {
	setlocale(LC_ALL, "RU");

	Tree elka;
	elka.name = "Ёлка";
	elka.ages = 14;
	elka.get_all_info();

	return 0;


}