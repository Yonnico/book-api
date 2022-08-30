from flask import request, abort

from api.author.db import all_authors
from api.book.db import all_books

from api.core.services import validate_for_str


def find_author_by_id(author_id):
    author = list(filter(lambda a: a['id'] == author_id, all_authors))
    return author


def add_books_to_author(author):
    books = list(filter(lambda b: b['author_id'] == author['id'], all_books))
    author_with_books = author.copy()
    author_with_books['books'] = books
    return author_with_books


def get_all_authors():
    return all_authors


def get_all_authors_with_books():
    return list(map(add_books_to_author, all_authors))


def is_author_id_exist(id):
    value = False
    for author in all_authors:
        if author['id'] == id:
            value = True
    return value


def remove_books_with_author(author):
    books = list(filter(lambda b: b['author_id'] == author['id'], all_books))
    for book in books:
        all_books.remove(book)
    all_authors.remove(author)
    return


def validate_author_id(val):
    return isinstance(val, int) and is_author_id_exist(val)


def validate_add_author(nickname, name):
    if not request.json:
        abort(400)
    if 'nickname' not in request.json:
        abort(400)
    if 'name' not in request.json:
        abort(400)
    if 'nickname' in request.json:
        if not validate_for_str(nickname):
            abort(400)
    if 'name' in request.json:
        if not validate_for_str(name):
            abort(400)
    id = all_authors[-1]['id'] + 1
    author = {
        'id': id,
        'nickname': nickname,
        'name': name
    }
    all_authors.append(author)
    return author