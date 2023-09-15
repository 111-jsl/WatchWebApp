from functools import wraps
def param_none2str(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        new_args = [i if i is not None else '' for i in args]
        return f(new_args, **kwargs)
    return decorated
