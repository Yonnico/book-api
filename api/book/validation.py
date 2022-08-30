from api.core.validation import is_str

def validate_title(val):
    return is_str(val) and len(val)


def validate_annotation(val):
    return is_str(val) and len(val)