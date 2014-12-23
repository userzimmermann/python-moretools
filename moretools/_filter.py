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

"""functions for filtering sequence elements by attr/item checking
"""

from ._common import *
from ._common import _map, _filter
from ._undefined import undefined


def filter(func, seq=undefined):
    """Replacement for builtin filter().

    - With both arguments it works like builtin filter()
      (itertools.ifilter() in PY2).
    - If only `func` is given, a new function is returned,
      which only takes a sequence as argument and applies
      given `func` and this sequence to builtin filter(),
      which makes filter() also usable as decorator:

    .. code:: python

        @filter
        def func(item):
            ...
            return <True/False>

        filtered_seq = func(seq)
    """
    if seq is undefined:
        def filter(seq):
            return _filter(func, seq)

        filter.__name__ = func.__name__
        return filter

    return _filter(func, seq)


def filtermethod(func):
    """Decorator for turning methods into filter methods,
       which filter items from given sequences
       depending on the boolean truth of the return values
       from calling `func` with each item from the sequence.

    - Works like :func:`moretools.filter` if only called with `func` argument,
      but additionally handles the _self_ argument of given `func`.
    """
    def filter(self, seq):
        return _filter(partial(func, self), seq)

    filter.__name__ = func.__name__
    return filter


def filterattrs(seq, *attrs, **attrs_and_values):
    return _filter(
      lambda seqitem: all(chain(
        _map(partial(hasattr, seqitem), attrs),
        starmap(lambda attr, value: getattr(seqitem, attr) == value,
                attrs_and_values.items()))),
      seq)


def filteritems(seq, **keys_and_values):
    return _filter(
      lambda seqitem: all(chain(
        _map(partial(hasitem, seqitem), keys),
        starmap(lambda key, value: seqitem[key] == value,
                keys_and_values.items()))),
      seq)


## def filterkeys(, **keys_and_values):
