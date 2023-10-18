# include <iostream>

using namespace std;

int main()
{
	setlocale(LC_ALL, "Ru");
	double gallons, liters;

	cout << "Введите кол-во галлонов:";
	cin >> gallons;
	liters = gallons * 4;
	cout << "Литров: " << liters;
	return 0;
}