#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <fstream>
#include <Windows.h>

using namespace std;

class Service {
private:
    string serviceName;
    double cost;

public:
    Service(string name = "", double price = 0.0) : serviceName(name), cost(price) {}

    void displayServiceInfo() const {
        cout << left << setw(30) << serviceName << "| Стоимость: " << fixed << setprecision(2) << cost << " руб." << endl;
    }

    double getCost() const {
        return cost;
    }

    string getName() const {
        return serviceName;
    }

    friend ofstream& operator<<(ofstream& ofs, const Service& service) {
        ofs << service.serviceName << endl << service.cost << endl;
        return ofs;
    }

    friend ifstream& operator>>(ifstream& ifs, Service& service) {
        getline(ifs, service.serviceName);
        ifs >> service.cost;
        ifs.ignore();
        return ifs;
    }
};

class Client {
private:
    string name;
    string phoneNumber;

public:
    Client() {}

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

    // Геттер для имени клиента
    string getName() const {
        return name;
    }

    friend ofstream& operator<<(ofstream& ofs, const Client& client) {
        ofs << client.name << endl << client.phoneNumber << endl;
        return ofs;
    }

    friend ifstream& operator>>(ifstream& ifs, Client& client) {
        getline(ifs, client.name);
        getline(ifs, client.phoneNumber);
        return ifs;
    }
};

class Car {
private:
    string model;
    string licensePlate;

public:
    Car() {}

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

    friend ofstream& operator<<(ofstream& ofs, const Car& car) {
        ofs << car.model << endl << car.licensePlate << endl;
        return ofs;
    }

    friend ifstream& operator>>(ifstream& ifs, Car& car) {
        getline(ifs, car.model);
        getline(ifs, car.licensePlate);
        return ifs;
    }
};

class Mechanic {
private:
    string name;
    int experience;

public:
    Mechanic() {}

    void inputMechanicInfo() {
        cout << "Введите имя механика: ";
        getline(cin, name);
        cout << "Введите стаж механика (лет): ";
        cin >> experience;
        cin.ignore();
    }

    void displayMechanicInfo() const {
        cout << left << setw(20) << "Имя механика:" << name << endl;
        cout << left << setw(20) << "Стаж:" << experience << " лет" << endl;
    }

    friend ofstream& operator<<(ofstream& ofs, const Mechanic& mechanic) {
        ofs << mechanic.name << endl << mechanic.experience << endl;
        return ofs;
    }

    friend ifstream& operator>>(ifstream& ifs, Mechanic& mechanic) {
        getline(ifs, mechanic.name);
        ifs >> mechanic.experience;
        ifs.ignore();
        return ifs;
    }
};

class Order {
private:
    Client client;
    Car car;
    Mechanic mechanic;
    vector<Service> availableServices;
    vector<Service> selectedServices;

public:
    Order() {
        availableServices.push_back(Service("Замена масла", 1500.00));
        availableServices.push_back(Service("Ремонт тормозов", 3000.00));
        availableServices.push_back(Service("Диагностика двигателя", 2500.00));
        availableServices.push_back(Service("Балансировка колес", 1000.00));
    }

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
        cin.ignore();
    }

    void displayOrderInfo() const {
        if (selectedServices.empty()) {
            cout << "\nНет заказов для отображения." << endl;
            return;
        }

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

    // Сохранение данных в файл
    void saveOrderToFile(ofstream& ofs) {
        ofs << client << car << mechanic;
        for (const auto& service : selectedServices) {
            ofs << service;
        }
    }

    // Загрузка данных из файла
    void loadOrderFromFile(ifstream& ifs) {
        ifs >> client >> car >> mechanic;
        Service service;
        while (ifs >> service) {
            selectedServices.push_back(service);
        }
    }

    string getClientName() const {
        return client.getName();
    }
};

class OrderManager {
private:
    vector<Order> orders;

public:
    void addOrder() {
        Order order;
        order.inputOrderInfo();
        orders.push_back(order);
    }

    void displayOrders() const {
        if (orders.empty()) {
            cout << "Нет заказов для отображения." << endl;
            return;
        }

        for (size_t i = 0; i < orders.size(); ++i) {
            cout << "\n=== Заказ #" << i + 1 << " ===" << endl;
            orders[i].displayOrderInfo();
        }
    }

    void deleteOrder() {
        if (orders.empty()) {
            cout << "Нет заказов для удаления." << endl;
            return;
        }

        int index;
        cout << "Введите номер заказа для удаления: ";
        cin >> index;
        if (index > 0 && index <= orders.size()) {
            orders.erase(orders.begin() + index - 1);
            cout << "Заказ удалён." << endl;
        }
        else {
            cout << "Неверный номер заказа." << endl;
        }
    }

    void editOrder() {
        if (orders.empty()) {
            cout << "Нет заказов для редактирования." << endl;
            return;
        }

        int index;
        cout << "Введите номер заказа для редактирования: ";
        cin >> index;
        if (index > 0 && index <= orders.size()) {
            orders[index - 1].inputOrderInfo();
            cout << "Заказ обновлён." << endl;
        }
        else {
            cout << "Неверный номер заказа." << endl;
        }
    }

    void searchOrder() const {
        if (orders.empty()) {
            cout << "Нет заказов для поиска." << endl;
            return;
        }

        string searchName;
        cout << "Введите имя клиента для поиска: ";
        cin.ignore();
        getline(cin, searchName);

        bool found = false;
        for (const auto& order : orders) {
            if (order.getClientName() == searchName) {
                order.displayOrderInfo();
                found = true;
            }
        }

        if (!found) {
            cout << "Заказ с таким именем клиента не найден." << endl;
        }
    }

    void saveAllOrders(const string& filename) {
        ofstream ofs(filename);
        if (!ofs) {
            cout << "Ошибка открытия файла для записи!" << endl;
            return;
        }
        for (auto& order : orders) {  // убираем const, чтобы можно было вызвать неконстантный метод
            order.saveOrderToFile(ofs);
        }

        ofs.close();
        cout << "Все заказы сохранены." << endl;
    }

    void loadAllOrders(const string& filename) {
        ifstream ifs(filename);
        if (!ifs) {
            cout << "Ошибка открытия файла для чтения!" << endl;
            return;
        }
        while (!ifs.eof()) {
            Order order;
            order.loadOrderFromFile(ifs);
            orders.push_back(order);
        }
        ifs.close();
        cout << "Все заказы загружены." << endl;
    }
};

int main() {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    OrderManager manager;
    int choice;

    while (true) {
        cout << "\n1. Ввести новый заказ" << endl;
        cout << "2. Отобразить все заказы" << endl;
        cout << "3. Удалить заказ" << endl;
        cout << "4. Редактировать заказ" << endl;
        cout << "5. Найти заказ" << endl;
        cout << "6. Сохранить все заказы в файл" << endl;
        cout << "7. Загрузить заказы из файла" << endl;
        cout << "8. Выйти" << endl;
        cout << "Выберите действие: ";
        cin >> choice;

        switch (choice) {
        case 1:
            manager.addOrder();
            break;
        case 2:
            manager.displayOrders();
            break;
        case 3:
            manager.deleteOrder();
            break;
        case 4:
            manager.editOrder();
            break;
        case 5:
            manager.searchOrder();
            break;
        case 6:
            manager.saveAllOrders("orders.txt");
            break;
        case 7:
            manager.loadAllOrders("orders.txt");
            break;
        case 8:
            return 0;
        default:
            cout << "Неверный выбор!" << endl;
        }
    }

    return 0;
}
