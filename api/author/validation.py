from api.core.validation import is_str, is_int
from api.author.db import all_authors

def is_author_id_exist(id):
    value = False
    for author in all_authors:
        if author['id'] == id:
            value = True
    return value


def validate_nickname(val):
    return is_str(val) and len(val)


def validate_name(val):
    return is_str(val) and len(val)


def validate_author_id(val):
    return is_int(val) and is_author_id_exist(val)