#include <iostream>
#include <string>


using namespace std;

template<typename T>
void print_arr(T* arr, int len) {
	for (int i = 0; i < len; i++) {
		cout << *(arr + i)<< "";
	}
	cout << endl;
}


int main() {
	setlocale(LC_ALL, "RU");

	int arr1[] = { 5, 6 ,3,2, 1,0 };
	print_arr<int>(arr1, 6);

	float arr2[] = { 5.34f, 6.01f };
	print_arr<float>(arr2, 2);

	return 0;
}