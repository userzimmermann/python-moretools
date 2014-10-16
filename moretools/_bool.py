__all__ = ['booltype', 'isbooltype', 'isbool']


class Bool(object):
    def __init__(self, value):
        cls = type(self)
        if isbool(value):
            self.value = bool(value)
        elif value in cls.true:
            self.value = True
        elif value in cls.false:
            self.value = False
        else:
            raise ValueError(repr(value))

    def __nonzero__(self):
        return self.value

    def __repr__(self):
        return repr(self.value)


def booltype(typename='Bool', true=None, false=None, base=Bool):
    ## , strict=True):

    if not issubclass(base, Bool):
        raise TypeError("'base' is no subclass of booltype.base: %s"
                        % base)

    class Type(type):
        pass

    Type.true = true
    Type.false = false

    ## Type.strict = strict

    ## def __init__(self, value):
    ##     cls = type(self)
    ##     self.value = bool(value in cls.true
    ##       or value not in cls.false and value)

    return Type(typename, (base,), {}) ## '__init__': __init__})


booltype.base = Bool


def isbooltype(cls):
    return issubclass(cls, (bool, Bool))


def isbool(obj):
    return isinstance(obj, (bool, Bool))
