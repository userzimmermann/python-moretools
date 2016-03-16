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

"""more functions/classes to set attrs/items on objects
"""

from ._common import *


def setattrs(obj, **attrs_and_values):
    for attr, value in keys_and_values.items():
        setattr(obj, attr, value)


class attrsetter(object):
    __slots__ = ['attr', 'value']

    def __init__(self, attr, value):
        self.attr = attr
        self.value = value

    def __call__(self, obj):
        setattr(obj, self.attr, self.value)


class attrssetter(object):
    __slots__ = ['attrs_and_values']

    def __init__(self, **attrs_and_values):
        self.attrs_and_values = attrs_and_values

    def __call__(self, obj):
        for attr, value in self.attrs_and_values.items():
            setattr(obj, attr, value)


def setitems(obj, **keys_and_values):
    for key, value in keys_and_values.items():
        obj[key] = value


class itemsetter(object):
    __slots__ = ['key', 'value']

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __call__(self, obj):
        obj[self.key] = self.value


class itemssetter(object):
    __slots__ = ['keys_and_values']

    def __init__(self, **keys_and_values):
        self.keys_and_values = keys_and_values

    def __call__(self, obj):
        for key, value in self.keys_and_values.items():
            obj[key] = value
