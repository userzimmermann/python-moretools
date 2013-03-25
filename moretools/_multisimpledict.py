# python-moretools
#
# many more basic tools for python 2/3
# extending itertools, functools and operator
#
# Copyright (C) 2011-2013 Stefan Zimmermann <zimmermann.code@gmail.com>
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
__all__ = (
  'MultiSimpleDictType',
  'SimpleDictSetType', 'simpledictset',
  'SimpleDictZipType', 'simpledictzip',
  )

from ._common import *

from ._multidict import *
from ._multidict import _NoValue, _MultiDictBase

class _MultiSimpleDictMeta(type):
  def __init__(cls, clsname, bases, clsattrs):
    if not hasattr(cls, 'iterate'):
      return
    iter_func = getattr(cls, '_iter_' + cls.iterate)
    cls.__iter__ = lambda self: iter_func(self)

  def _iter_keys(cls, self):
    return iter(set(chain(*(d.__dict__.keys() for d in self.__dicts__))))

  def _iter_items(cls, self):
    for key in cls._iter_keys(self):
      yield key, self[key]

  def _iter_values(cls, self):
    for key in cls._iter_keys(self):
      yield self[key]

class MultiSimpleDictType(_MultiDictBase):
  def __getattr__(self, name):
    raise NotImplementedError

  def __dir__(self):
    return list(set(chain(*(dir(d) for d in self.__dicts__))))

class _SimpleDictSetMeta(_MultiSimpleDictMeta):
  class MultipleKey(LookupError):
    pass

  MultipleKey.__name__ = 'SimpleDictSet.MultipleKey'

  class MultipleAttribute(LookupError):
    pass

  MultipleAttribute.__name__ = 'SimpleDictSet.MultipleAttribute'

class SimpleDictSetType(MultiSimpleDictType):
  __metaclass__ = _SimpleDictSetMeta

  def __getitem__(self, key):
    cls = type(self) # holds the helper methods and custom options
    ivalues = (d.__dict__.get(key, _NoValue) for d in self.__dicts__)
    values = [v for v in ivalues if v is not _NoValue]
    if not values:
      raise KeyError(key)
    if len(values) > 1:
      if cls.multiple_key_handler:
        return cls.multiple_key_handler(key, values)
      else:
        raise cls.MultipleKey(key)
    return values[0]

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

def simpledictset(
  typename, iterate = 'items',
  multiple_key_handler = None, multiple_attr_handler = None,
  basetype = SimpleDictSetType
  ):
  if not issubclass(basetype, SimpleDictSetType):
    raise TypeError(
      "Custom `basetype` must be derived from %s." % repr(
        SimpleDictSetType))
  metaclsattrs = dict(
    iterate = iterate,
    multiple_key_handler = staticmethod(multiple_key_handler),
    multiple_attr_handler = staticmethod(multiple_attr_handler),
    )
  metacls = type(typename + 'Meta', (type(basetype),), metaclsattrs)
  return metacls(typename, (basetype,), {})

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
  typename, iterate = 'items', default_value = _NoValue,
  basetype = SimpleDictZipType
  ):
  if not issubclass(basetype, SimpleDictZipType):
    raise TypeError(
      "Custom `basetype` must be derived from %s." % repr(
        SimpleDictZipType))
  metaclsattrs = dict(
    iterate = iterate,
    default_value = default_value,
    )
  metacls = type(typename + 'Meta', (type(basetype),), metaclsattrs)
  return metacls(typename, (basetype,), {})
