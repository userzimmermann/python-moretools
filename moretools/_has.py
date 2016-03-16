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

"""moretools._has

[Deprecated] More functions/classes to check avaiability
of attrs/items on objects.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six.moves import map


def hasattrs(obj, *attrs):
    return map(partial(hasattr, obj), attrs)


class attrtester(object):
    __slots__ = ['attr']

    def __init__(self, attr):
        self.attr = attr

    def __call__(self, obj):
        return hasattr(obj, self.attr)


class attrstester(object):
    __slots__ = ['attrs']

    def __init__(self, *attrs):
        self.attrs = attrs

    def __call__(self, obj):
        return hasattrs(obj, *self.attrs)


class itemtester(object):
    __slots__ = ['key', 'value']

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __call__(self, obj):
        return obj[key] == self.value


class itemstester(object):
    __slots__ = ['keys_and_values']

    def __init__(self, **keys_and_values):
        self.keys_and_values = keys_and_values

    def __call__(self, obj):
        for key, value in self.keys_and_values:
            yield obj[key] == value
