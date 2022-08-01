from flask import request, abort

from api.author.db import all_authors
from api.book.db import all_books

from api.author.services import validate_author_id

def find_book_by_id(book_id):
    book = list(filter(lambda b: b['id'] == book_id, all_books))
    return book


def add_author_to_book(book):
    author = list(filter(lambda a: a['id'] == book['author_id'], all_authors))
    author = author[0]
    book_with_author = book.copy()
    book_with_author.pop('author_id')
    book_with_author['author'] = author
    return book_with_author


def get_all_books():
    return all_books


def get_all_books_with_authors():
    return list(map(add_author_to_book, all_books))


def delete_book_from_all_books(book):
    return all_books.remove(book)


def validate_title(val):
    return isinstance(val, str) and len(val)


def validate_annotation(val):
    return isinstance(val, str) and len(val)


def validate_add_book(title, annotation, author_id):
    if not request.json:
        abort(400)
    if not 'title' in request.json:
        abort(400)
    if not 'annotation' in request.json:
        abort(400)
    if not 'author_id' in request.json:
        abort(400)
    if 'title' in request.json:
        if not validate_title(title):
            abort(400)
    if 'annotation' in request.json:
        if not validate_annotation(annotation):
            abort(400)
    if 'author_id' in request.json:
        if not validate_author_id(author_id):
            abort(400)

    id = all_books[-1]['id'] + 1
    book = {
        'id': id,
        'title': title,
        'annotation': annotation,
        'author_id': author_id
    }

    all_books.append(book)
    return book
    