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

Functions for getting iterators of dictionary keys/values/items
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
    if not isdict(d):
        raise TypeError("dictkeys() arg must be a dictionary")
    if issimpledict(d):
        d = d.__dict__
    return six.iterkeys(d)


def dictvalues(d):
    if not isdict(d):
        raise TypeError("dictvalues() arg must be a dictionary")
    if issimpledict(d):
        d = d.__dict__
    return six.itervalues(d)


def dictitems(d):
    if not isdict(d):
        raise TypeError("dictitems() arg must be a dictionary")
    if issimpledict(d):
        d = d.__dict__
    return six.iteritems(d)


def dictfilter(func, d=undefined, key=undefined, value=undefined):
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
