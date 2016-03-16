# python-moretools
#
# many more basic tools for python 2/3
# extending itertools, functools and operator
#
# Copyright (C) 2011-2016 Stefan Zimmermann <zimmermann.code@gmail.com>
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

"""moretools._lazy

Lazy collection implementations.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['Lazy', 'LazyDict']

from ._common import *


class Lazy(partial):
    """Just a little `partial` wrapper
       to support unique lazy value type checking in :class:`LazyDict`.
    """
    pass


class LazyDict(dict):
    """A `dict` wrapper checking values for being of type :class:`Lazy`.

    - Lazy values will be evaluated on first [key] access
      or use of :meth:`call()`.
    - Lazy values don't show up in :meth:`.values()` and :meth:`.items()`.
    """

    def __getitem__(self, key):
        value = dict.__getitem__(self, key)
        if isinstance(value, Lazy):
            value = self[key] = value()
        return value

    def call(self, key, *args, **kwargs):
        value = dict.__getitem__(self, key)
        if not isinstance(value, Lazy):
            raise TypeError("%s value is not a Lazy instance." % repr(key))
        value = self[key] = value(*args, **kwargs)
        return value

    def values(self):
        for value in dict.values(self):
            if type(value) is not Lazy:
                yield value

    def items(self):
        for key, value in dict.items(self):
            if type(value) is not Lazy:
                yield key, value
