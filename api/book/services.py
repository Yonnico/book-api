from flask import request

from api.author.db import all_authors
from api.book.db import all_books

from api.book.validation import validate_annotation, validate_title
from api.author.validation import validate_author_id



def get_book_by_id(book_id):
    book = list(filter(lambda b: b['id'] == book_id, all_books))
    if len(book):
        return book[0]
    return None


def get_author_to_book(book):
    author = list(filter(lambda a: a['id'] == book['author_id'], all_authors))
    author = author[0]
    book_with_author = book.copy()
    book_with_author.pop('author_id')
    book_with_author['author'] = author
    return book_with_author


def get_all_books():
    return all_books


def get_all_books_with_authors():
    return list(map(get_author_to_book, all_books))


def remove_book(book):
    return all_books.remove(book)


def validate_and_add_book(title, annotation, author_id):
    if not private_validate_book(title, annotation, author_id):
        return None
    return private_add_book(title, annotation, author_id)


def private_validate_book(title, annotation, author_id):
    if not request.json:
        return None
    if not 'title' in request.json:
        return None
    if not 'annotation' in request.json:
        return None
    if not 'author_id' in request.json:
        return None
    if 'title' in request.json:
        if not validate_title(title):
            return None
    if 'annotation' in request.json:
        if not validate_annotation(annotation):
            return None
    if 'author_id' in request.json:
        if not validate_author_id(author_id):
            return None
    return True


def private_add_book(title, annotation, author_id):
    id = all_books[-1]['id'] + 1
    book = {
        'id': id,
        'title': title,
        'annotation': annotation,
        'author_id': author_id
    }

    all_books.append(book)
    return book


def validate_and_change_book(book_id, title, annotation, author_id):
    book = get_book_by_id(book_id)
    if not book:
        return {'status': 0, 'value': None}
    if title is not None and not validate_title(title):
        return {'status': 1, 'value': title}
    if annotation is not None and not validate_annotation(annotation):
        return {'status': 1, 'value': annotation}
    if author_id is not None and not validate_author_id(author_id):
        return {'status': 1, 'value': author_id}
    if title is not None:
        book['title'] = title
    if annotation is not None:
        book['annotation'] = annotation
    if author_id is not None:
        book['author_id'] = author_id
    return {'status': 2, 'value': book}