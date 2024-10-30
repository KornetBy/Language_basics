#include <iostream>
#include <string>

using namespace std;


class PC {
private:
	int diagonal;
	string os;
public:
	PC(int diagonal, string os) {
		this->diagonal = diagonal;
		this->os = os;
	}
	void get_info() {
		cout << "Diagonal = " << this->diagonal << ", os -  " << this->os << endl;
	}
};

class Laptop : public PC {
private: 
	float weight;
public:
	Laptop(int diagonal, string os, float weight):PC(diagonal, os) {
		this->weight = weight;
	

	}
	void get_info() {
		PC::get_info();
		cout << "Weight: " << this->weight <<endl;
	}
};

int main() {
	setlocale(LC_ALL, "RU");

	PC Legion(24, "Windows");

	Laptop mac(16, "Mac", 1.5f);
	mac.get_info();
	return 0;
}