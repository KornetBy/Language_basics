#include <iostream>
#include <string>
#include <cmath>
#include <cstring>


using namespace std;

int main() {
	setlocale(LC_ALL, "RU");

	string str1 = "Hello ";
	string str2 = "World";

	//str1.append(str2);
	str1 += str2;
	
	str1.pop_back();
	str1.push_back('!');
	cout << str1.length()<< endl;

	cout << pow(2, 3) << endl;

	cout << abs(-5) << endl;
	cout << sqrt(16) << endl;

	cout << ceil(1.2232f) << "\n"<< floor(1.2232f) << "\n" << round(1.2232f) << endl;

	return 0;
}