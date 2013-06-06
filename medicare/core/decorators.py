from django.utils.decorators import method_decorator


@method_decorator
def provides_context(fn):
    def wraps(*args, **kwargs):
        return fn(*args, **kwargs)
    wraps.provides_context = True
    wraps.__name__ = fn.__name__
    wraps.__doc__ = fn.__doc__
    return wraps
