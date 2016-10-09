"""
A module for adding a call/cc feature to Python.
"""

__version__ = '0.1'

__internal_type_error__ = (
    "Argument of a continuation must be a continuable function."
    )

class _Continuation(Exception):
    def __init__(self, f, args, kwargs):
        self.func, self.args, self.kwargs = f, args, kwargs

class Continuation():
    def __init__(self, calling_id):
        self.calling_id = calling_id
    def __callback__(self, f):
        if isinstance(f, _Continuation):
            f.uid = id(self)
            raise f
        raise TypeError(__internal_type_error__)
    def __call__(self, f):
        return lambda *args, **kwargs: self.__callback__(f(*args, **kwargs))
    __lshift__ = __call__

def with_continuation(func):
    def _w(*args, **kwargs):
        return _Continuation(func, args, kwargs)
    _w.__with_continuation_signature__ = True
    return _w

class _with_CC():
    def __call__(self, f):
        try:
            _ = f.__with_continuation_signature__
        except AttributeError:
            raise TypeError(__internal_type_error__)
        return (
            lambda *args, **kwargs:
                _with_CC().__callback__(f(*args, **kwargs)))
    __rshift__ = __call__
    def __callback__(self, f):
        k = Continuation(id(self))
        i = id(k)
        while True:
            try:
                return (f.func)(k)(*f.args, **f.kwargs)
            except _Continuation as e:
                if i == e.uid: f = e
                else: raise e

with_CC = _with_CC()
