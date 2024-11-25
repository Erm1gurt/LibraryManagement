from books import Book
from manage import Manage


class Library:
    def __init__(self):
        self.move = {
            '0': '',
            '1': self.add_book,
            '2': self.del_book,
            '3': self.search_book,
            '4': self.view_book,
            '5': self.change_book_status
        }
        self.manage = Manage()

    @staticmethod
    def is_next(move: str) -> bool:
        next_book = input(f'  Хотите {move} другую книгу?\n'
                          '\t1 - Да\n'
                          '\t0 - Нет\n'
                          '  Укажите число: ')
        while next_book not in ['1', '0']:
            next_book = input('\tУказано некорректное число, попробуйте снова: ')
        return bool(int(next_book))

    @staticmethod
    def set_char_fild(massage: str, error_massage: str) -> str:
        fild = input(massage)
        while not fild:
            fild = input(error_massage)
        return fild

    @staticmethod
    def set_num_fild(massage: str, error_massage: str) -> int:
        fild = input(massage)
        while not fild or not fild.isalnum() or not int(fild):
            fild = input(error_massage)
        return int(fild)

    def return_menu_or_close(self):
        move = input('\n  Хотите вернуться в меню или завершить работу?\n'
                     '\t0 - Завершить работу\n'
                     '\t1 - Вернуться в меню\n'
                     '  Укажите число: ')
        while move not in ['0', '1']:
            move = input('\tУказано некорректное число, попробуйте снова: ')
        if move == '1':
            print()
            self.main_menu()

    def main_menu(self) -> None:
        print('Добро пожаловать в систему управления данными библиотеки\n'
              '  Вы можете перейти в раздел:\n'
              '\t1. Добавления книги\n'
              '\t2. Удаления книги\n'
              '\t3. Поиска книг\n'
              '\t4. Просмотра списока всех книг\n'
              '\t5. Измения статуса книги\n'
              '\t0. Завершение работы')
        move = input('  Укажите номер нужного раздела: ')
        while move not in self.move:
            move = input('  Номер указан не корректно, попробуйте снова: ')
        if move == '0':
            return
        self.move[move]()

    def add_book(self, next_book: bool = False) -> None:
        if not next_book:
            print('\nВы перешли в раздел добавления книги')
        print('  Чтобы добавить книгу укажите')

        title = self.set_char_fild('\t1. Название книги: ', '  Поле название книги не может быть пустым, укажите название: ')
        author = self.set_char_fild('\t2. Автора: ', '  Поле автор не может быть пустым, укажите автора: ')
        year = self.set_num_fild('\t3. Год издания: ',
                             '  Поле год не может быть пустым. Год может быть только числом больше, попробуйте снова: ')

        self.manage.add_book(title, author, int(year))

        next_book = self.is_next(move='добавить')
        if next_book:
            self.add_book(next_book)

        if not next_book:
            self.manage.write_db()
            print('\t\tКниги добавлены')
            self.return_menu_or_close()

    def del_book(self, next_book: bool = False) -> None:
        if not next_book:
            print('\nВы перешли в раздел добавления книги')
        print('  Чтобы удалить книгу укажите')
        book_id = self.set_num_fild('\t1. УИД книги: ',
                                    '  УИД не может быть пустым. УИД может быть только числом больше 0, попробуйте снова: ')
        is_del = self.manage.del_book(book_id)
        if is_del:
            print('Книга удалена')
        else:
            print('Книги с таким УИД не было в БД')

        next_book = self.is_next(move='удалить')
        if next_book:
            self.del_book(next_book)

        if not next_book:
            self.manage.write_db()
            self.return_menu_or_close()

    def search_book(self):
        print('\nВы перешли в раздел поиска книг')
        print('  Чтобы найти книги укажите')
        search_query = self.set_char_fild('\t Название книги, Автора или Год издания: ',
                                          '  Поле поиска не может быть пустым, попробуйте снова')
        books_list = self.manage.search_book(search_query.lower())
        if books_list:
            self.manage.view_books(books_list)
        else:
            print('Книги по заданным параметрам не найдены')
            next_book = self.is_next(move='найти')
            if next_book:
                self.search_book()

        self.return_menu_or_close()

    def view_book(self):
        print('\n\tСписок всех книг: ')
        self.manage.view_books()
        self.return_menu_or_close()

    def change_book_status(self, next_book: bool = False):
        print('\nВы перешли в раздел изменения статуса книг')
        print('  Чтобы изменить статус книги укажите')
        book_id = self.set_num_fild('\t1. УИД книги: ',
                                    '  УИД не может быть пустым. УИД может быть только числом больше 0, попробуйте снова: ')
        status = input(f'\t2. Новый статус ("{list(Book.statuses)[0]}" или "{list(Book.statuses)[1]}"): ').lower()
        while status not in Book.statuses.keys():
            status = input('  Новый статус указан не корректно, попробуйте снова: ').lower()
        is_change = self.manage.change_book_status(book_id, status)
        if is_change:
            print('Статус книги изменен')
        else:
            print('Стутус книги был такой же, либо книга с таким УИД отсутствует в БД')

        next_book = self.is_next(move='изменить')
        if next_book:
            self.change_book_status(next_book)

        if not next_book:
            self.manage.write_db()
            self.return_menu_or_close()

if __name__ == '__main__':
    menu = Library()
    menu.main_menu()

