from flask import abort

def validate_len(val):
    if not len(val):
        return abort(404)
    return
