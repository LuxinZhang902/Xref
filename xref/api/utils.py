
# only get the first error for now
def get_error_msg(serializer_errors):
    field = ''
    error_msg = ''
    for f, errors in serializer_errors.items():
        field = f
        for e in errors:
            error_msg += e
        break
    return field, error_msg