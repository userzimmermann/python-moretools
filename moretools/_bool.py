# python-moretools
#
# many more basic tools for python 2/3
# extending itertools, functools and operator
#
# Copyright (C) 2011-2014 Stefan Zimmermann <zimmermann.code@gmail.com>
#
# python-moretools is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-moretools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with python-moretools.  If not, see <http://www.gnu.org/licenses/>.

from six import with_metaclass

__all__ = ['boolclass', 'booltype', 'isboolclass', 'isbooltype', 'isbool']

from inspect import isclass


class Type(type):
    def __contains__(cls, value):
        return isbool(value) or value in cls.true or value in cls.false


class Bool(with_metaclass(Type, object)):
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


def boolclass(typename='Bool', true=None, false=None, base=Bool):
    ## , strict=True):

    if not issubclass(base, Bool):
        raise TypeError("'base' is no subclass of boolclass.base: %s"
                        % base)

    class Type(type(base)):
        pass

    Type.true = true
    Type.false = false

    ## Type.strict = strict

    ## def __init__(self, value):
    ##     cls = type(self)
    ##     self.value = bool(value in cls.true
    ##       or value not in cls.false and value)

    return Type(typename, (base,), {}) ## '__init__': __init__})

booltype = boolclass


boolclass.base = Bool


def isboolclass(cls):
    if not isclass(cls):
        return False
    return issubclass(cls, (bool, Bool))

isbooltype = isboolclass


def isbool(obj):
    return isinstance(obj, (bool, Bool))
