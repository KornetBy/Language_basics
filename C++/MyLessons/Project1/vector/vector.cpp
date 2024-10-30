#include <iostream>
#include <vector>

int main() {
    // Создание вектора целых чисел
    std::vector<int> numbers;

    // Добавление элементов в вектор
    numbers.push_back(10);
    numbers.push_back(20);
    numbers.push_back(30);

    // Доступ к элементам вектора по индексу
    std::cout << "First element: " << numbers[0] << std::endl;
    std::cout << "Second element: " << numbers[1] << std::endl;

    // Размер вектора
    std::cout << "Vector size: " << numbers.size() << std::endl;

    // Перебор элементов вектора с использованием цикла
    for (size_t i = 0; i < numbers.size(); i++) {
        std::cout << "Element " << i << ": " << numbers[i] << std::endl;
    }

    return 0;
}
