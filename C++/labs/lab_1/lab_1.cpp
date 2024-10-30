
#include <iostream>//потоки ввода/вывода
#include <vector>
#include <string>
#include <iomanip> // Для использования флагов выравнивания
#include <Windows.h> 

using namespace std;

// Класс Service: представляет услугу
class Service {
private:
    string serviceName;
    double cost;

public:
    Service(string name = "", double price = 0.0) : serviceName(name), cost(price) {}

    void displayServiceInfo() const {
        cout << left << setw(30) << serviceName << "| Стоимость: " << fixed << setprecision(2) << cost << " руб." << endl;//setprecision(streamsize Prec); Задает точность для значений с плавающей запятой
    }

    double getCost() const {
        return cost;
    }

    string getName() const {
        return serviceName;
    }
};

// Класс Client: содержит данные о клиенте
class Client {
private:
    string name;
    string phoneNumber;

public:
    Client() {}

    // Ввод данных о клиенте
    void inputClientInfo() {
        cout << "Введите имя клиента: ";
        getline(cin, name);
        cout << "Введите номер телефона клиента: ";
        getline(cin, phoneNumber);
    }

    void displayClientInfo() const {
        cout << left << setw(20) << "Имя клиента:" << name << endl;
        cout << left << setw(20) << "Телефон клиента:" << phoneNumber << endl;
    }
};

// Класс Car: информация об автомобиле
class Car {
private:
    string model;
    string licensePlate;

public:
    Car() {}

    // Ввод данных о машине
    void inputCarInfo() {
        cout << "Введите модель автомобиля: ";
        getline(cin, model);
        cout << "Введите номерной знак автомобиля: ";
        getline(cin, licensePlate);
    }

    void displayCarInfo() const {
        cout << left << setw(20) << "Модель автомобиля:" << model << endl;
        cout << left << setw(20) << "Номерной знак:" << licensePlate << endl;
    }
};

// Класс Mechanic: содержит информацию о механике
class Mechanic {
private:
    string name;
    int experience;  // опыт работы в годах

public:
    Mechanic() {}

    // Ввод данных о механике
    void inputMechanicInfo() {
        cout << "Введите имя механика: ";
        getline(cin, name);
        cout << "Введите стаж механика (лет): ";
        cin >> experience;
        cin.ignore();  // очистка буфера после ввода числа
    }

    void displayMechanicInfo() const {
        cout << left << setw(20) << "Имя механика:" << name << endl;
        cout << left << setw(20) << "Стаж:" << experience << " лет" << endl;
    }
};

// Класс Order: включает информацию о заказе
class Order {
private:
    Client client;
    Car car;
    Mechanic mechanic;
    vector<Service> availableServices; // список доступных услуг
    vector<Service> selectedServices;  // список выбранных услуг

public:
    Order() {
        // Предустановленные услуги
        availableServices.push_back(Service("Замена масла", 1500.00));
        availableServices.push_back(Service("Ремонт тормозов", 3000.00));
        availableServices.push_back(Service("Диагностика двигателя", 2500.00));
        availableServices.push_back(Service("Балансировка колес", 1000.00));
    }

    // Ввод данных заказа
    void inputOrderInfo() {
        cout << "\n=== Введите данные клиента ===" << endl;
        client.inputClientInfo();

        cout << "\n=== Введите данные автомобиля ===" << endl;
        car.inputCarInfo();

        cout << "\n=== Введите данные механика ===" << endl;
        mechanic.inputMechanicInfo();

        cout << "\n=== Доступные услуги ===" << endl;
        for (size_t i = 0; i < availableServices.size(); ++i) {
            cout << i + 1 << ". ";
            availableServices[i].displayServiceInfo();
        }

        
        int serviceIndex;
        char addMore = 'y';
        while (addMore == 'y' || addMore == 'Y') {
            cout << "\nВведите номер услуги, которую хотите добавить: ";
            cin >> serviceIndex;
            if (serviceIndex > 0 && serviceIndex <= availableServices.size()) {
                selectedServices.push_back(availableServices[serviceIndex - 1]);
                cout << "Услуга добавлена: " << availableServices[serviceIndex - 1].getName() << endl;
            }
            else {
                cout << "Неверный номер услуги!" << endl;
            }

            cout << "Хотите добавить еще одну услугу? (y/n): ";
            cin >> addMore;
        }
    }

    // Отображение полной информации о заказе
    void displayOrderInfo() const {
        cout << "\n===== Информация о заказе =====" << endl;
        client.displayClientInfo();
        car.displayCarInfo();
        mechanic.displayMechanicInfo();

        cout << "\nВыбранные услуги: " << endl;
        double totalCost = 0.0;
        for (const auto& service : selectedServices) {
            service.displayServiceInfo();
            totalCost += service.getCost();
        }
        cout << left << setw(30) << "Общая стоимость:" << totalCost << " руб." << endl;
    }
};

int main() {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    Order order;

    // Ввод данных о заказе
    order.inputOrderInfo();

    // Отображение информации о заказе
    order.displayOrderInfo();

    return 0;
}