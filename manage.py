import json
import os.path

from books import Book


class Manage:
    '''
    Класс для управления библиотечными данными
    '''
    def __init__(self):
        self.db = 'books_db.json'
        self.max_id = 0
        self.book_list = self.open_db()

    def open_db(self) -> list[Book]:
        '''
        Функция открывает БД с книгами и десериализует данные.
        :returns: Список книг
        '''

        books_list = []

        if not os.path.isfile(self.db):
            return books_list

        with open(self.db, 'r', encoding='utf-8') as json_file:
            books_data = json.load(json_file)

        for key, val in books_data.items():
            book = Book(int(key), val['title'], val['author'], val['year'], val['status'])
            books_list.append(book)
            self.max_id = max(self.max_id, int(key))

        return books_list

    def write_db(self) -> None:
        '''
        Функция записывает добавленные книг в БД
        '''

        books_data = {}
        for book in self.book_list:
            books_data[book.book_id] = {
                'title': book.title,
                'author': book.author,
                'year': book.year,
                'status': book.status
            }

        with open(self.db, 'w', encoding='utf-8') as json_file:
            json.dump(books_data, json_file, indent=4, ensure_ascii=False)

    def add_book(self, title: str, author: str, year: int) -> None:
        '''
        Функция для создания экземлпяра книги
        :param title: Название
        :param author: Автор
        :param year: Год издания
        :return:
        '''
        self.max_id += 1
        book = Book(self.max_id, title, author, year, status=True)
        self.book_list.append(book)

    def del_book(self, book_id: int) -> bool:
        '''
        Функция для удаления книги из БД
        :param book_id: УИД книги, которую нужно удалить
        :return: True, если книга удалена, False если такой книги не было в БД
        '''
        for ind, book in enumerate(self.book_list):
            if book.book_id == book_id:
                self.book_list.pop(ind)
                return True
        return False

    def search_book(self, search_query: str) -> list[Book]:
        '''
        Функция принимает строку поиска и возвращает список книг, которые имеют полное/частичное совпадение по
        одному из полей: Название книги, Автор или Год издания
        :param search_query: строка, которую пользователь указал при поиске книги
        :return: список книг, попавших под совпадение с поиском
        '''
        result = []
        for book in self.book_list:
            if search_query in [book.title.lower(), book.author.lower(), str(book.year)]:
                result.append(book)
                continue
            if search_query in book.title.lower():
                result.append(book)
                continue
            if search_query in book.author.lower():
                result.append(book)
                continue
        return result


    def view_books(self, book_list: list[Book] | None = None) -> None:
        '''
        Функция для вывода списка книг
        :param book_list: список книг, необязательный параметр, используется для вывода книг в частом случае (из
        функции поиска)
        :return:
        '''
        if not book_list and not self.book_list:
            print('В библиотеке пока нет ни одной книги')

        for book in book_list or self.book_list:
            print(book)

    def change_book_status(self, book_id: int, status: str):
        '''
        Функция для изменения статуса существующей в БД книги
        :param book_id: УИД книги, у которой нужно изменить статус
        :param status: новый статус книги
        :return: True если статус был изменен, False если такой книги нет в БД или статус не был изменен
        '''
        for ind, book in enumerate(self.book_list):
            if book.book_id == book_id and book.status != Book.statuses[status]:
                book.status = Book.statuses[status]
                return True
        return False


if __name__ == '__main__':
    manage = Manage()
