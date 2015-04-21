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

"""moretools._bool

Tools for creating custom bool classes with .true and .false value lists.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = ['boolclass', 'booltype', 'isboolclass', 'isbooltype', 'isbool']

from inspect import isclass
from functools import total_ordering


class Meta(type):
    """Base metaclass for :func:`moretools.boolclass` creator.
    """
    def __contains__(cls, value):
        """Check if `value` is a valid initialization value for
           :class:`moretools.Bool`-derived `cls`.
        """
        return isbool(value) or value in cls.true or value in cls.false


@total_ordering
class Bool(with_metaclass(Meta, object)):
    """Base class for :func:`moretools.boolclass` creator.
    """
    def __init__(self, value):
        """Initialize with True or False
           by checking if `value` is a builtin bool or Bool-derived value
           or is contained in the custom .true or .false list
           of the own Bool-derived class.
        """
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

    def __eq__(self, value):
        return isbool(value) and self.value == bool(value)

    def __lt__(self, value):
        if not isbool(value):
            raise TypeError("Unorderable types: %s and %s" % (
              type(self), type(value)))
        return self.value < bool(value)

    def __repr__(self):
        return repr(self.value)


def boolclass(typename='Bool', true=None, false=None, base=Bool):
    """Create a custom bool class which can only be initialized
       with builtin bool values, instances of boolclass()-created classes
       or values contained in the given `true` or `false` sequence.

    - Optionally takes a custom `base` class,
      which must be derived from default boolclass.base
    """
    ## , strict=True):

    if not issubclass(base, Bool):
        raise TypeError("'base' is no subclass of boolclass.base: %s"
                        % base)

    # store true and false lists as metaclass attributes
    # to keep it away from instances of created class
    class Meta(type(base)):
        pass

    Meta.true = true
    Meta.false = false

    ## Meta.strict = strict

    return Meta(typename, (base,), {})

booltype = boolclass


boolclass.base = Bool


def isboolclass(cls):
    """Check if `cls` is builtin bool
       or a :func:`moretools.boolclass`-created class.
    """
    if not isclass(cls):
        return False
    return issubclass(cls, (bool, Bool))

isbooltype = isboolclass


def isbool(obj):
    """Check if `obj` is a builtin bool
       or an instance of a :func:`moretools.boolclass`-created class.
    """
    return isinstance(obj, (bool, Bool))
