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

"""several extended repeat generator functions
with attr/item or call returning
"""
__all__ = ['repeatcall', 'repeatattr', 'repeatitem']

from six.moves import map
from functools import partial


def repeatcall(obj, times=-1):
    while times:
        if times > 0:
            times -= 1
        yield obj()


def repeatattr(obj, attr, times=-1):
    while times:
        if times > 0:
            times -= 1
        yield getattr(obj, attr)


def repeatattrs(obj, *attrs, **kwargs):
    times = kwargs.get('times', -1)
    while times:
        if times > 0:
            times -= 1
        yield map(partial(getattr, obj), attrs)


def repeatitem(obj, key, times=-1):
    while times:
        if times > 0:
            times -= 1
        yield obj[key]


def repeatitems(obj, *keys, **kwargs):
    times = kwargs.get('times', -1)
    while times:
        if times > 0:
            times -= 1
        yield map(partial(getitem, obj), keys)
