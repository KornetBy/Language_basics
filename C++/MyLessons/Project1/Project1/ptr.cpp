#include <iostream>


using namespace std;

int main() {

	const char* message = "Hello, World!";

	int x = 5;
	int* u;

	u = &x;
	*u = 6;
	cout << x<< endl;
	cout << u << endl;
	cout << message << endl;

	return 0;
}
