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

Tools for creating custom bool classes
with explicit ``.true`` and ``.false`` lists of valid instantiation values.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

from inspect import isclass
from functools import total_ordering

__all__ = ['StrictBoolMeta', 'StrictBool', 'strictbool',
           'isboolclass', 'isbool',
           # aliases for backwards compatibility
           'Bool', 'boolclass', 'booltype', 'isbooltype']


class StrictBoolMeta(type):
    """Metaclass for :class:`moretools.StrictBool`
       and base metaclass used in :func:`moretools.strictbool` class creator.
    """
    def __contains__(cls, value):
        """Check if `value` is a valid initialization value for
           :class:`moretools.StrictBool`-derived `cls`.
        """
        return isbool(value) or value in cls.true or value in cls.false


@total_ordering
class StrictBool(with_metaclass(StrictBoolMeta, object)):
    """Abstract base class for creating custom bool classes
       with explicit lists of accepted true and false values.

    - Derived classes just have to provide those true and false value lists
      as ``.true`` and ``.false`` class atrributes.
    - Also used as base class by :func:`moretools.strictbool` class creator.
    """
    def __new__(cls, value):
        if cls is StrictBool:
            raise TypeError("Can't instantiate abstract %s" % repr(cls))
        return object.__new__(cls)

    def __init__(self, value):
        """Initialize with builtin True or False
           or a :class:`StrictBool`-derived `value`
           or a `value` contained in either ``.true`` or ``.false`` list
           the of own :class:`StrictBool` derived class.

        - Instances are usable and comparable like builtin bool values.
        - Actual bool value gets stored as ``self.value``.
        """
        cls = type(self)
        if isbool(value):
            self.value = bool(value)
        elif cls.true is not None and value in cls.true:
            self.value = True
        elif cls.false is not None and value in cls.false:
            self.value = False
        else:
            raise ValueError(repr(value))

    def __bool__(self):
        return self.value

    # PY2
    __nonzero__ = __bool__

    def __eq__(self, value):
        return isbool(value) and self.value == bool(value)

    def __lt__(self, value):
        if not isbool(value):
            raise TypeError("Unorderable types: %s and %s"
                            % (repr(type(self)), repr(type(value))))
        return self.value < bool(value)

    def __int__(self):
        return int(self.value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        """Just True or False.
        """
        return repr(self.value)


# backwards compatibility
Bool = StrictBool


def strictbool(typename='Bool', true=None, false=None, base=Bool):
    """Create a custom bool class which can only be initialized
       with builtin bool values, instances of boolclass()-created classes
       or values contained in the given `true` or `false` sequences.

    - Optionally takes a custom `base` class,
      which must be derived from default ``strictbool.base``
      (:class:`moretools.StrictBool`).
    """
    if not issubclass(base, Bool):
        raise TypeError("%s is no subclass of strictbool.base"
                        % repr(base))

    class Meta(type(base)):
        """Metaclass created by moretools.strictbool.
        """
        pass

    # store true and false lists as metaclass attributes
    # to keep it away from instances of created class
    Meta.true = true
    Meta.false = false

    return Meta(typename, (base,), {})


strictbool.base = StrictBool

# backwards compatibility
booltype = boolclass = strictbool


def isboolclass(cls):
    """Check if `cls` is builtin ``bool``
       or a :class:`moretools.StrictBool`-derived class.
    """
    if not isclass(cls):
        return False
    return issubclass(cls, (bool, Bool))


# backwards compatiblity
isbooltype = isboolclass


def isbool(obj):
    """Check if `obj` is a builtin ``bool`` instance
       or an instance of a :func:`moretools.StrictBool`-derived class.
    """
    return isinstance(obj, (bool, StrictBool))
