#include <iostream>
#include <string>

using namespace std;

/*
int num = 10;
	int& a = num;
	cout << a <<endl;
	cout << &a<< endl;
	cout << &num << endl;
	cout << *(&num) << endl;
	return 0;*/

int minimal(int* arr, int len) {
	int min = *arr;
	for (int i = 0; i < len; i++) {
		if (min > *(arr + i))
			min = *(arr + i);
	
	}
	return min;
}


int main() {
	setlocale(LC_ALL, "RU");
	int arr[] = { 5, 7, 1,0,-9 };
	cout<< minimal(arr, 5);
}