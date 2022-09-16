from api.author.db import all_authors

from api.author.validation import validate_nickname, validate_name

#FOR CONTROLLER

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

#FOR VIEW

def get_author_by_id(author_id):
    author = list(filter(lambda a: a['id'] == author_id, all_authors))
    if len(author):
        return author[0]
    return None


def get_all_authors():
    return all_authors


def validate_and_add_author(nickname, name):
    if not private_validate_author(nickname, name, True):
        return None
    return private_add_author(nickname, name)


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
