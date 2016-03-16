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

"""More functions/classes to delete attrs/items on objects.
"""

from ._common import *


def delattrs(obj, *attrs):
    for attr in attrs:
        delattr(obj, attr)


class attrdeleter(object):
    __slots__ = ['attr']

    def __init__(self, attr):
        self.attr = attr

    def __call__(self, obj):
        delattr(obj, self.attr)


class attrsdeleter(object):
    __slots__ = ['attrs']

    def __init__(self, *attrs):
        self.attrs = attrs

    def __call__(self, obj):
        for attr in self.attrs:
            delattr(obj, attr)


def delitems(obj, *keys):
    for key in keys:
        del obj[key]


def itemdeleter(key):
    def del_(obj):
        del obj[key]

    return del_


def itemsdeleter(*keys):
    def del_(obj):
        for key in keys:
            del obj[key]

    return del_
