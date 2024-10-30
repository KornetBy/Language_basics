#include <iostream>
#include <string>

using namespace std;


template<class T>
class Arrays {
private:
	int len;
	T* arr;
public:
	Arrays(T* a, int len) {
		this->len = len;
		arr = new T[len];
		for (int i = 0; i < len; i++)
			*(this ->arr + i) = *(a + i);
	}
	void get() {
		for (int i = 0; i < len; i++)
			cout << *(arr + i) << " ";
	}

	~Arrays() {
		delete[]arr;
	}
};

int main() {
	setlocale(LC_ALL, "RU");

	int arr1[] = { 3, 5, 3 };
	float arr2[] = { 3.5f, 5.3f };
	Arrays<int> obj1(arr1, 3);
	Arrays<float> obj2(arr2, 2);
	obj1.get();
	obj2.get();

	return 0;
}