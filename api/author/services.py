from api.author.db import all_authors
from api.book.db import all_books

def add_books_to_author(author):
    books = list(filter(lambda b: b['author_id'] == author['id'], all_books))
    author_with_books = author.copy()
    author_with_books['books'] = books
    return author_with_books

def find_author_by_id(author_id):
    author = list(filter(lambda a: a['id'] == author_id, all_authors))
    return author


def is_author_id_exist(id):
    value = False
    for author in all_authors:
        if author['id'] == id:
            value = True
    return value