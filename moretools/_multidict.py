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

"""moretools._multidict

Various container types with a combined interface to multiple `dict`s.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['MultiDictType', 'DictSet', 'DictZip', 'DictStruct']

from six import with_metaclass

from ._common import *


class _NoValue:
    pass


class _MultiDictBase(object):
    def __init__(self, dicts):
        self.__dicts__ = list(dicts)

    def __len__(self):
        return len(set(chain(*(d.keys() for d in self.__dicts__))))

    def __getitem__(self, key):
        raise NotImplementedError

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.__dicts__))


class MultiDictType(_MultiDictBase):
    def keys(self):
        for key in set(chain(*(d.keys() for d in self.__dicts__))):
            yield key

    def values(self):
        for key in self.keys():
            yield self[key]

    def items(self):
        for key in self.keys():
            yield key, self[key]

    def __iter__(self):
        return self.keys()

    def __contains__(self, key):
        return key in self.keys()


class _DictSetMeta(type):
    class MultipleKey(LookupError):
        pass

    MultipleKey.__name__ = 'DictSet.MultipleKey'


class DictSet(with_metaclass(_DictSetMeta, MultiDictType)):
    def __getitem__(self, key):
        ivalues = (d.get(key, _NoValue) for d in self.__dicts__)
        values = [v for v in ivalues if v is not _NoValue]
        if not values:
            raise KeyError(key)
        if len(values) > 1:
            raise type(self).MultipleKey(key)
        return values[0]


class DictZip(MultiDictType):
    def __init__(self, dicts, default_value = _NoValue):
        super(type(self), self).__init__(self, dicts)

        if default_value is not _NoValue:
            self.default_value = default_value

    @property
    def _default_value(self):
        try:
            return self.default_value
        except AttributeError:
            return _NoValue

    def __getitem__(self, key):
        valuetuple = tuple(
          d.get(key, self._default_value) for d in self.__dicts__)
        if _NoValue in valuetuple:
            raise KeyError(key)
        return valuetuple


class DictStruct(MultiDictType, dict):
    def __init__(self, name, bases, mapping=None, **items):
        self.__name__ = name
        self.__bases__ = tuple(bases)
        if mapping is None:
            dict.__init__(self, **items)
        else:
            dict.__init__(self, mapping, **items)

    def __len__(self):
        return len(set(chain(
          dict.keys(self), *(d.keys() for d in self.__bases__))))

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            for d in self.__bases__:
                try:
                    return d[key]
                except KeyError:
                    pass
        raise KeyError(key)

    def keys(self):
        for key in set(chain(
          dict.keys(self), *(d.keys() for d in self.__bases__)
          )):
            yield key

    def __repr__(self):
        return '%s(%s, %s, %s)' % (
          type(self).__name__, repr(self.__name__), repr(self.__bases__),
          dict.__repr__(self))
