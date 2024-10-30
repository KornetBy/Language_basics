#include <iostream>
using namespace std;

int main(){
	setlocale(LC_ALL, "RU");
	int num1, num2;
	cout << "Введите число 1:";
	cin >> num1;

	cout << "Введите число 2:";
	cin >> num2;

	if (num1 < num2) {
		cout << "Число 1 меньше числа 2";
	}
	else if (num2 < num1) cout << "Число 2 меньше числа 1";
	else cout << "Числа равны";
}