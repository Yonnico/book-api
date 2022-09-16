from api.book.db import all_books

from api.author.services import get_all_authors, get_author_by_id

from api.book.validation import validate_annotation, validate_title
from api.author.validation import validate_author_id

#FOR CONTROLLER

def private_validate_book(title, annotation, author_id, required):
    if required or title != None :
        if not validate_title(title):
            return False
    if required or annotation != None:
        if not validate_annotation(annotation):
            return False
    if required or author_id != None:
        if not validate_author_id(author_id):
            return False
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


def get_link_by_author(book):
    authors = get_all_authors()
    author = list(filter(lambda a: a['id'] == book['author_id'], authors))
    return author


def get_link_by_book(author):
    book = list(filter(lambda b: b['author_id'] == author['id'], all_books))
    return book


def get_author_with_book(author):
    books = list(filter(lambda b: b['author_id'] == author['id'], all_books))
    author_with_books = author.copy()
    author_with_books['books'] = books
    return author_with_books


def get_book_with_author(book):
    author = get_link_by_author(book)
    author = author[0]
    book_with_author = book.copy()
    book_with_author.pop('author_id')
    book_with_author['author'] = author
    return book_with_author

#FOR VIEW

def get_book_by_id(book_id):
    book = list(filter(lambda b: b['id'] == book_id, all_books))
    if len(book):
        return book[0]
    return None


def get_book_with_author_by_id(book_id):
    book = get_book_by_id(book_id)
    author = get_link_by_author(book)
    book_with_author = book.copy()
    book_with_author.pop('author_id')
    book_with_author['author'] = author
    return book_with_author


def remove_author_with_books(author_id):
    authors = get_all_authors()
    author = get_author_by_id(author_id)
    if author != None:
        books = get_link_by_book(author)
        for book in books:
            all_books.remove(book)
        return authors.remove(author)
    return False


def get_author_with_book_by_id(author_id):
    author = get_author_by_id(author_id)
    books = list(filter(lambda b: b['author_id'] == author['id'], all_books))
    author_with_books = author.copy()
    author_with_books['books'] = books
    return author_with_books


def get_authors_with_books():
    authors = get_all_authors()
    return list(map(get_author_with_book, authors))


def get_all_books():
    return all_books


def get_books_with_authors():
    return list(map(get_book_with_author, all_books))


def remove_book(book_id):
    book = get_book_by_id(book_id)
    if book != None:
        return all_books.remove(book)
    return False


def validate_and_add_book(title, annotation, author_id):
    if not private_validate_book(title, annotation, author_id, True):
        return None
    return private_add_book(title, annotation, author_id)


def validate_and_change_book(book_id, title, annotation, author_id):
    book = get_book_by_id(book_id)
    if not book:
        return {'status': 0, 'value': None}
    if not private_validate_book(title, annotation, author_id, False):
        return {'status': 1, 'value': None}
    if title != None:
        book['title'] = title
    if annotation != None:
        book['annotation'] = annotation
    if author_id != None:
        book['author_id'] = author_id
    return {'status': 2, 'value': book}