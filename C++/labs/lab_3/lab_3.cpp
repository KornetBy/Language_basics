#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <algorithm>  // для std::sort
#include <iomanip>    // для форматированного вывода
#include <windows.h>  // для SetConsoleCP и SetConsoleOutputCP

using namespace std;

// Класс Book: представляет книгу
class Book {
private:
    string title;
    string author;
    int year;

public:
    // Конструктор
    Book(string t, string a, int y) : title(t), author(a), year(y) {}

    // Геттеры
    string getTitle() const { return title; }
    string getAuthor() const { return author; }
    int getYear() const { return year; }

    // Методы для изменения данных книги
    void setTitle(const string& t) { title = t; }
    void setAuthor(const string& a) { author = a; }
    void setYear(int y) { year = y; }

    // Метод для вывода информации о книге
    void display() const {
        cout << left << setw(20) << "Название: " << title << endl;
        cout << left << setw(20) << "Автор: " << author << endl;
        cout << left << setw(20) << "Год выпуска: " << year << endl;
        cout << "------------------------------" << endl;
    }

    // Перегрузка операторов для записи/чтения в/из файла
    friend ofstream& operator<<(ofstream& ofs, const Book& book) {
        ofs << book.title << endl << book.author << endl << book.year << endl;
        return ofs;
    }

    friend ifstream& operator>>(ifstream& ifs, Book& book) {
        getline(ifs, book.title);
        getline(ifs, book.author);
        ifs >> book.year;
        ifs.ignore();
        return ifs;
    }
};

// Класс для управления книгами
class BookManager {
private:
    vector<Book> books;  // Контейнер для хранения книг

public:
    // Добавление новой книги
    void addBook() {
        string title, author;
        int year;

        cout << "Введите название книги: ";
        cin.ignore();
        getline(cin, title);

        cout << "Введите автора книги: ";
        getline(cin, author);

        cout << "Введите год выпуска: ";
        cin >> year;

        books.emplace_back(title, author, year);
        cout << "Книга добавлена!" << endl;
    }

    // Удаление книги по названию
    void deleteBook() {
        string title;
        cout << "Введите название книги для удаления: ";
        cin.ignore();
        getline(cin, title);

        auto it = remove_if(books.begin(), books.end(), [&](const Book& book) {
            return book.getTitle() == title;
            });

        if (it != books.end()) {
            books.erase(it, books.end());
            cout << "Книга удалена!" << endl;
        }
        else {
            cout << "Книга не найдена!" << endl;
        }
    }

    // Редактирование книги по названию
    void editBook() {
        string title;
        cout << "Введите название книги для редактирования: ";
        cin.ignore();
        getline(cin, title);

        auto it = find_if(books.begin(), books.end(), [&](const Book& book) {
            return book.getTitle() == title;
            });

        if (it != books.end()) {
            string newTitle, newAuthor;
            int newYear;

            cout << "Введите новое название: ";
            getline(cin, newTitle);
            cout << "Введите нового автора: ";
            getline(cin, newAuthor);
            cout << "Введите новый год выпуска: ";
            cin >> newYear;

            it->setTitle(newTitle);
            it->setAuthor(newAuthor);
            it->setYear(newYear);

            cout << "Книга отредактирована!" << endl;
        }
        else {
            cout << "Книга не найдена!" << endl;
        }
    }

    // Поиск книги по названию
    void searchBook() {
        string title;
        cout << "Введите название книги для поиска: ";
        cin.ignore();
        getline(cin, title);

        auto it = find_if(books.begin(), books.end(), [&](const Book& book) {
            return book.getTitle() == title;
            });

        if (it != books.end()) {
            cout << "Книга найдена!" << endl;
            it->display();
        }
        else {
            cout << "Книга не найдена!" << endl;
        }
    }

    // Фильтрация книг по автору
    void filterByAuthor() {
        string author;
        cout << "Введите автора для фильтрации: ";
        cin.ignore();
        getline(cin, author);

        cout << "Книги автора " << author << ":" << endl;
        for (const auto& book : books) {
            if (book.getAuthor() == author) {
                book.display();
            }
        }
    }

    // Сортировка книг по году выпуска
    void sortByYear() {
        sort(books.begin(), books.end(), [](const Book& a, const Book& b) {
            return a.getYear() < b.getYear();
            });
        cout << "Книги отсортированы по году выпуска!" << endl;
    }

    // Вывод всех книг на экран
    void displayBooks() const {
        if (books.empty()) {
            cout << "Список книг пуст." << endl;
            return;
        }

        for (const auto& book : books) {
            book.display();
        }
    }

    // Сохранение всех книг в файл
    void saveToFile(const string& filename) {
        ofstream ofs(filename);
        if (!ofs.is_open()) {
            cout << "Ошибка открытия файла для записи!" << endl;
            return;
        }

        for (const auto& book : books) {
            ofs << book;
        }

        ofs.close();
        cout << "Данные сохранены в файл!" << endl;
    }

    // Загрузка книг из файла
    void loadFromFile(const string& filename) {
        ifstream ifs(filename);
        if (!ifs.is_open()) {
            cout << "Ошибка открытия файла для чтения!" << endl;
            return;
        }

        books.clear();
        Book book("", "", 0);
        while (ifs >> book) {
            books.push_back(book);
        }

        ifs.close();
        cout << "Данные загружены из файла!" << endl;
    }
};

// Меню для взаимодействия с программой
void showMenu() {
    cout << "1. Добавить книгу" << endl;
    cout << "2. Удалить книгу" << endl;
    cout << "3. Редактировать книгу" << endl;
    cout << "4. Поиск книги" << endl;
    cout << "5. Фильтрация по автору" << endl;
    cout << "6. Сортировка по году" << endl;
    cout << "7. Вывести все книги" << endl;
    cout << "8. Сохранить книги в файл" << endl;
    cout << "9. Загрузить книги из файла" << endl;
    cout << "0. Выход" << endl;
}

int main() {
    // Устанавливаем кодировку для поддержки русского языка
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    BookManager manager;
    int choice;
    string filename = "books.txt";

    while (true) {
        showMenu();
        cout << "Выберите действие: ";
        cin >> choice;

        switch (choice) {
        case 1:
            manager.addBook();
            break;
        case 2:
            manager.deleteBook();
            break;
        case 3:
            manager.editBook();
            break;
        case 4:
            manager.searchBook();
            break;
        case 5:
            manager.filterByAuthor();
            break;
        case 6:
            manager.sortByYear();
            break;
        case 7:
            manager.displayBooks();
            break;
        case 8:
            manager.saveToFile(filename);
            break;
        case 9:
            manager.loadFromFile(filename);
            break;
        case 0:
            return 0;
        default:
            cout << "Неверный выбор!" << endl;
        }
    }

    return 0;
}
