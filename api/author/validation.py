from api.core.validation import is_str, is_int
from api.author.db import all_authors

def is_author_id_exist(id):
    for author in all_authors:
        if author['id'] == id:
            return True
    return False


def validate_nickname(val):
    return val != None and is_str(val) and len(val)


def validate_name(val):
    return val != None and is_str(val) and len(val)


def validate_author_id(val):
    return val != None and is_int(val) and is_author_id_exist(val)