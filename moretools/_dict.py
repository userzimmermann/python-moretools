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

"""moretools._dict

Functions for Python 2/3-unified iteration of dictionary keys/values/items
and filtering dictionary items,
which also work with simpledict instances.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""

__all__ = ['dictkeys', 'dictvalues', 'dictitems', 'dictfilter']

from ._common import *
from ._undefined import undefined
from ._simpledict import issimpledict
from ._types import isdict

import six


def dictkeys(d):
    """Iterate the keys of dictionary `d` in a Python 2/3-unified way.

    - Also supports func:`moretools.simpledict` instances.
    """
    if not isdict(d):
        raise TypeError("dictkeys() arg must be a dictionary")
    if issimpledict(d):
        d = d.__dict__
    return six.iterkeys(d)


def dictvalues(d):
    """Iterate the values of dictionary `d` in a Python 2/3-unified way.

    - Also supports func:`moretools.simpledict` instances.
    """
    if not isdict(d):
        raise TypeError("dictvalues() arg must be a dictionary")
    if issimpledict(d):
        d = d.__dict__
    return six.itervalues(d)


def dictitems(d):
    """Iterate the (key, value) pairs of dictionary `d`
       in a Python 2/3-unified way.

    - Also supports func:`moretools.simpledict` instances.
    """
    if not isdict(d):
        raise TypeError("dictitems() arg must be a dictionary")
    if issimpledict(d):
        d = d.__dict__
    return six.iteritems(d)


def dictfilter(func, d=undefined, key=undefined, value=undefined):
    """Filter the (key, value) pairs of dictionary `d`
       by iterating all pairs for which:

    1. The filter `func`, called with key and value as separate arguments,
       returns a True value.
    2. The comparisons of key and value
       with the optional `key=` and `value=` args are True.

    - `func` may be None to only check against `key=` and `value=` args.
    - If no dictionary is given,
      a ``functools.partial()``-like object is returned,
      which can later be called with a dictionary argument
      and is therefore usable for functional expressions like ``map(...)``
    - Also supports func:`moretools.simpledict` instances.
    """
    def filter(d):
        for k, v in dictitems(d):
            if func is not None and not func(k, v):
                continue
            if key is not undefined and key != k:
                continue
            if value is not undefined and value != v:
                continue
            yield k, v

    if d is undefined:
        filter.__name__ = func.__name__
        return filter

    return filter(d)
