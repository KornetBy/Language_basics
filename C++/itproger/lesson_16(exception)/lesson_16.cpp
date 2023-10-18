#include <iostream>
#include <string>


using namespace std;

void divide(float a, float b) {
	if (b == 0) throw (100);
	else
		cout << (a / b);
}

int main() {
	setlocale(LC_ALL, "RU");
	
	try {
		divide(5.2f, 0.0f);
	}
	catch (int err) {
		if (err == 100) cout << "Ошибка при делении на 0";
	}
	
	return 0;
}