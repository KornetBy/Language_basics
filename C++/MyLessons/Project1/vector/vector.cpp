#include <iostream>
#include <vector>

int main() {
    // �������� ������� ����� �����
    std::vector<int> numbers;

    // ���������� ��������� � ������
    numbers.push_back(10);
    numbers.push_back(20);
    numbers.push_back(30);

    // ������ � ��������� ������� �� �������
    std::cout << "First element: " << numbers[0] << std::endl;
    std::cout << "Second element: " << numbers[1] << std::endl;

    // ������ �������
    std::cout << "Vector size: " << numbers.size() << std::endl;

    // ������� ��������� ������� � �������������� �����
    for (size_t i = 0; i < numbers.size(); i++) {
        std::cout << "Element " << i << ": " << numbers[i] << std::endl;
    }

    return 0;
}
