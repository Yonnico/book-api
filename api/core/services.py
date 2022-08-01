from flask import abort

def validate_len(val):
    if not len(val):
        abort(404)
    return
