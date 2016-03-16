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

"""moretools._multisimpledict

Various container types with a combined interface to multiple `simpledict`s.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = [
  'MultiSimpleDictType',
  'SimpleDictSetType', 'simpledictset',
  'SimpleDictZipType', 'simpledictzip',
  ]

from ._common import *

from ._multidict import *
from ._multidict import _NoValue, _MultiDictBase


class MultiSimpleDictMeta(type):
    def keys(cls, self):
        return iter(set(chain(*(
          d.__dict__.keys() for d in self.__dicts__))))

    def items(cls, self):
        for key in type(cls).keys(cls, self):
            yield key, self[key]

    def values(cls, self):
        for key in type(cls).keys(cls, self):
            yield self[key]


class MultiSimpleDictType(_MultiDictBase):
    def __iter__(self):
        cls = type(self) # holds the helper methods and custom options
        # Get the custom specified iterate functions from metaclass
        # to allow overrides in custom derived classes:
        iter_func = getattr(type(cls), cls.iterate)
        return iter(iter_func(cls, self))

    def __getattr__(self, name):
        raise NotImplementedError

    def __dir__(self):
        return list(set(chain(*(dir(d) for d in self.__dicts__))))

    def __contains__(self, item):
        return item in iter(self)


class SimpleDictSetMeta(MultiSimpleDictMeta):
    class MultipleKeyError(LookupError):
        pass

    MultipleKeyError.__name__ = 'simpledictset.MultipleKeyError'
    # Backwards compatibility:
    MultipleKey = MultipleKeyError

    class MultipleAttributeError(LookupError):
        pass

    MultipleAttributeError.__name__ = 'simpledictset.MultipleAttributeError'
    # Backwards compatibility:
    MultipleAttribute = MultipleAttributeError


class SimpleDictSetType(
  with_metaclass(SimpleDictSetMeta, MultiSimpleDictType)
  ):
    def __getitem__(self, key):
        cls = type(self) # holds the helper methods and custom options
        ## ivalues = (d.__dict__.get(key, _NoValue) for d in self.__dicts__)

        def values():
            for d in self.__dicts__:
                try:
                    yield d[key]
                except KeyError:
                    yield _NoValue

        values = [v for v in values() if v is not _NoValue]
        if not values:
            raise KeyError(key)
        if len(values) > 1:
            if cls.multiple_key_handler:
                return cls.multiple_key_handler(key, values)
            else:
                raise cls.MultipleKey(key)
        return values[0]

    def __setitem__(self, key, value):
        cls = type(self)
        dicts = [d for d in self.__dicts__ if key in d.__dict__]
        if not dicts:
            raise KeyError(key)
        if len(dicts) > 1:
            raise cls.MultipleKey(key)
        dicts[0][key] = value

    def __getattr__(self, name):
        cls = type(self) # holds the helper methods and custom options
        ivalues = (getattr(d, name, _NoValue) for d in self.__dicts__)
        values = [v for v in ivalues if v is not _NoValue]
        if not values:
            raise AttributeError(name)
        if len(values) > 1:
            if cls.multiple_attr_handler:
                return cls.multiple_attr_handler(name, values)
            else:
                raise cls.MultipleAttribute(name)
        return values[0]

    def __setattr__(self, name, value):
        cls = type(self)
        if name.startswith('__'):
            object.__setattr__(self, name, value)
            return
        dicts = [d for d in self.__dicts__ if name in dir(d)]
        if not dicts:
            raise AttributeError(name)
        if len(dicts) > 1:
            raise cls.MultipleAttribute(name)
        setattr(dicts[0], name, value)

    def __add__(self, other):
        cls = type(self)
        if cls is not type(other):
            raise TypeError
        return cls(self.__dicts__ + other.__dicts__)


def simpledictset(
  typename, iterate='items',
  multiple_key_handler=None, multiple_attr_handler=None,
  basetype=SimpleDictSetType,
  extra = {},
  ):
    if not issubclass(basetype, SimpleDictSetType):
        raise TypeError(
          "Custom `basetype` must be derived from %s." % repr(
            SimpleDictSetType))
    metaclassattrs = dict(
      extra,
      iterate = iterate,
      multiple_key_handler = staticmethod(multiple_key_handler),
      multiple_attr_handler = staticmethod(multiple_attr_handler),
      )
    metaclass = type(typename + 'Meta', (type(basetype),), metaclassattrs)
    return metaclass(typename, (basetype,), {})


simpledictset.MultipleKeyError = SimpleDictSetType.MultipleKeyError
simpledictset.MultipleAttributeError = SimpleDictSetType.MultipleAttributeError


class SimpleDictZipType(MultiSimpleDictType):
    def __getitem__(self, key):
        cls = type(self) # holds the helper methods and custom options
        valuetuple = tuple(
          d.__dict__.get(key, cls.default_value) for d in self.__dicts__)
        if _NoValue in valuetuple:
            raise KeyError(key)
        return valuetuple

    def __getattr__(self, name):
        cls = type(self) # holds the helper methods and custom options
        valuetuple = tuple(
          getattr(d, name, cls.default_value) for d in self.__dicts__)
        if _NoValue in valuetuple:
            raise AttributeError(name)
        return valuetuple


def simpledictzip(
  typename, iterate='items', default_value=_NoValue,
  basetype=SimpleDictZipType
  ):
    if not issubclass(basetype, SimpleDictZipType):
        raise TypeError(
          "Custom `basetype` must be derived from %s." % repr(
            SimpleDictZipType))
    metaclassattrs = dict(
      iterate = iterate,
      default_value = default_value,
      )
    metaclass = type(typename + 'Meta', (type(basetype),), metaclassattrs)
    return metaclass(typename, (basetype,), {})
