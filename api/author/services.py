from api.author.db import all_authors
from api.book.db import all_books

from api.author.validation import validate_nickname, validate_name


def get_author_by_id(author_id):
    author = list(filter(lambda a: a['id'] == author_id, all_authors))
    if len(author):
        return author[0]
    return None


def get_author_with_book(author):
    books = list(filter(lambda b: b['author_id'] == author['id'], all_books))
    author_with_books = author.copy()
    author_with_books['books'] = books
    return author_with_books


def get_all_authors():
    return all_authors


def get_authors_with_books():
    return list(map(get_author_with_book, all_authors))


def remove_author_with_books(author_id):
    author = get_author_by_id(author_id)
    if len(author):
        books = list(filter(lambda b: b['author_id'] == author['id'], all_books))
        for book in books:
            all_books.remove(book)
        return all_authors.remove(author)
    return False


def validate_and_add_author(nickname, name):
    if not private_validate_author(nickname, name, True):
        return None
    return private_add_author(nickname, name)


def private_validate_author(nickname, name, required):
    if required or nickname != None:
        if not validate_nickname(nickname):
            return False
    if required or name != None:
        if not validate_name(name):
            return False
    return True

def private_add_author(nickname, name):
    id = all_authors[-1]['id'] + 1
    author = {
        'id': id,
        'nickname': nickname,
        'name': name
    }
    all_authors.append(author)
    return author


def validate_and_change_author(author_id, nickname, name):
    author = get_author_by_id(author_id)
    if not author:
        return {'status': 0, 'value': None}
    if not private_validate_author(author_id, nickname, name, False):
        return {'status': 1, 'value': None}
    if 'nickname' != None:
        author['nickname'] = nickname
    if 'name' != None:
        author['name'] = name
    return {'status': 2, 'value': author}
