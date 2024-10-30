#include <iostream>
using namespace std;

void myfun();

int main() {
	setlocale(LC_ALL, "RU");
	cout << "Вызов подпрограммы\n"<< abs(-1)<<".";
	myfun();

	return 0;
}

void myfun() {
	cout << "Вызванная подпрограмма";
}


