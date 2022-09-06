from api.core.validation import is_str

def validate_title(val):
    return val != None and is_str(val) and len(val)


def validate_annotation(val):
    return val != None and is_str(val) and len(val)