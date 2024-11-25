class Book:
    statuses = {
        'в наличии': True,
        'выдана': False
    }
    def __init__(self, book_id: int, title: str, author: str, year: int, status: bool):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return (f'{self.book_id}) {self.author}: {self.title}, год: {self.year}. '
                f'Книга {list(Book.statuses)[0] if self.status else list(Book.statuses)[1]}')


if __name__ == '__main__':
    book = Book(1, 'Руслан и Людмила', 'А.С. Пушкин', 1820, True)
    print(book)
