#include <iostream>


using namespace std;

void print(string word) {
	cout << word << endl;
}

void print(int word) {
	cout << word << endl;
}

void add(int a, int b) {
	int res = a + b;
	print(res);
}

int main() {

	setlocale(LC_ALL, "RU");
	print("lsfds");
	add(5, 6);

}