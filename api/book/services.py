from api.author.db import all_authors
from api.book.db import all_books

def add_author_to_book(book):
    author = list(filter(lambda a: a['id'] == book['author_id'], all_authors))
    author = author[0]
    book_with_author = book.copy()
    book_with_author.pop('author_id')
    book_with_author['author'] = author
    return book_with_author


def find_book_by_id(book_id):
    book = list(filter(lambda b: b['id'] == book_id, all_books))
    return book