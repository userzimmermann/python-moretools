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

"""moretools._simpledict

Provides the `simpledict` *mapping* type
and *exception* types for invalid *key*<-->*attrname* conversions.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = 'SimpleDictType', 'simpledict',

import re as _re

from ._common import *

class KeyToAttrError(AttributeError):
  def __init__(self, msg, key, attrname):
    AttributeError.__init__(self, '%s: %s' % (msg, (key, attrname)))

class KeyToAttrToKeyMismatch(LookupError):
  def __init__(self, key, attrname, key_from_attr):
    LookupError.__init__(self, (key, attrname, key_from_attr))

class AttrToKeyToAttrMismatch(LookupError):
  def __init__(self, attrname, key, attr_from_key):
    LookupError.__init__(self, (attrname, key, attr_from_key))

class SimpleDictMeta(type):
  """The basic meta class for :class:`SimpleDictType`.
  * Provides methods and attributes for *key*<-->*attrname* conversion checks
  to make them only be avaiable at type level, not at instance level.
  * :func:`simpledict` creates derived meta classes,
  which additionally hold the custom options
  (internal mapping type and *key*<-->*attrname* conversion functions).
  """
  _re_attrname = _re.compile('^[A-Za-z_][A-Za-z0-9_]*$')

  def _check_attr(cls, key, attrname):
    """Check (`key`-->)`attrname` validity.
    """
    if not cls._re_attrname.match(attrname):
      if attrname.startswith('__'):
        raise KeyToAttrError(
          "Attribute names must not start with '__'",
          key, attrname)
      raise KeyToAttrError(
        "Invalid Python identifier", key, attrname)

  def _reverse_check_key(cls, key, attrname):
    """Check reverse (`key`-->)`attrname`-->key conversion.
    """
    key_from_attr = cls.attr_to_key(attrname)
    if key_from_attr != key:
      raise KeyToAttrToKeyMismatch(key, attrname, key_from_attr)

  def _reverse_check_attr(cls, attrname, key):
    """Check reverse (`attrname`-->)`key`-->attr conversion.
    """
    attr_from_key = cls.key_to_attr(key)
    if attr_from_key != attrname:
      raise AttrToKeyToAttrMismatch(attrname, key, attr_from_key)

class SimpleDictType(object):
  """A simple *mapping* type providing item value access
  with `__getattr__`/`__setattr__`,
  using custom *key*<-->*attrname* conversion functions
  and a customizeable internal mapping type (defaults to `dict`).

  * Don't instantiate this class directly,
  use :func:`simpledict` to create a customized derived class
  * All custom options are stored in a custom meta class,
  which is also created by the `simpledict` function.
  * Attribute name representations of mapping keys
  must **not** start with '__'.
  * Automatically checks for valid *key*<-->*attrname* conversions
  on item insertion.
  * Doesn't provide any **non**-*special methods*.
  * `.__iter__()` returns an items (key/value pairs) iterator.
  """
  __metaclass__ = SimpleDictMeta

  def __init__(self, mapping = (), **items):
    """Instantiate the SimpleDictType with optional initial values.
    """
    cls = type(self) # holds the helper methods and custom options
    self.__dict__ = cls.dicttype(mapping, **items)
    for key in self.__dict__.keys():
      attrname = cls.key_to_attr(key)
      # check attribute name validity
      # *raises* `KeyToAttrError`
      cls._check_attr(key, attrname)
      # check reverse attr-->key conversion
      # *raises* `KeyToAttrToKeyMismatch`
      cls._reverse_check_key(key, attrname)

  def __getattr__(self, name):
    cls = type(self) # holds the helper methods and custom options
    try:
      key = cls.attr_to_key(name)
      return self.__dict__[key]
    except KeyError:
      raise AttributeError(name)

  def __setattr__(self, name, value):
    cls = type(self) # holds the helper methods and custom options
    if name.startswith('__'): # is real (internal) attribute?
      object.__setattr__(self, name, value)
    else: # convert name to key and store in `self.__dict__`
      key = cls.attr_to_key(name)
      # check reverse key-->attr conversion
      # *raises* `AttrToKeyToAttrMismatch`
      cls._reverse_check_attr(name, key)
      # accept name/value pair
      self.__dict__[key] = value

  def __delattr__(self, name):
    cls = type(self) # holds the helper methods and custom options
    if name.startswith('__'): # is real (internal) attribute?
      raise AttributeError(name)
    key = cls.attr_to_key(name)
    del self.__dict__[key]

  def __dir__(self):
    cls = type(self) # holds the helper methods and custom options
    return [cls.key_to_attr(key) for key in self.__dict__.keys()]

  def __iter__(self):
    cls = type(self) # holds the helper methods and custom options
    iter_func = getattr(self.__dict__, cls.iterate)
    return iter(iter_func())

  def __contains__(self, item):
    return item in iter(self)

  def __len__(self):
    return len(self.__dict__)

  def __setitem__(self, key, value):
    cls = type(self) # holds the helper methods and custom options
    attrname = str(cls.key_to_attr(key))
    # check attribute name validity
    # *raises* `KeyToAttrError`
    cls._check_attr(key, attrname)
    # check reverse attr-->key conversion
    # *raises* `KeyToAttrToKeyMismatch`
    cls._reverse_check_key(key, attrname)
    # accept the key/value pair
    self.__dict__[key] = value

  def __getitem__(self, key):
    return self.__dict__[key]

  def __delitem__(self, key):
    del self.__dict__[key]

  def __repr__(self):
    return 'simpledict(%s)' % repr(self.__dict__)

class SimpleFrozenDictType(object):
  """The :class:`SimpleDictType`
  without support for setting values after instantiation.
  * Custom frozen simpledict types are generated
  together with the normal custom simpledict types in :func:`simpledict`,
  stored as CustomType.frozen.
  """
  @classmethod
  def type(cls, simpledicttype = SimpleDictType):
    class SimpleFrozenDictType(cls, simpledicttype):
      def __setattr__(self, name, value):
        if name.startswith('__'): # is real (internal) attribute?
          object.__setattr__(self, name, value)
        else:
          raise NotImplementedError

      def __setitem__(self, name, value):
        raise NotImplementedError

    return SimpleFrozenDictType

def simpledict(
  typename, dicttype = dict, iterate = 'items',
  key_to_attr = lambda key: key, attr_to_key = lambda name: name,
  basetype = SimpleDictType,
  extra = {},
  ):
  """Create a custom :class:`SimpleDictType`-derived type.

  :param dicttype: The *mapping* type used for internal *item* storage.
  :param key_to_attr: The *function*
  used for items' *key*-->*attrname* conversions.
  :param attr_to_key: The *function*
  used for items' *attrname*-->*key* conversions.
  """
  if not issubclass(basetype, SimpleDictType):
    raise TypeError(
      "Custom `basetype` must be derived from %s." % repr(
        SimpleDictType))
  # first create a custom :class:`SimpleDictMeta`-derived meta type
  # holding the custom options
  metaclsattrs = dict(
    extra,
    dicttype = dicttype,
    iterate = iterate,
    key_to_attr = staticmethod(key_to_attr),
    attr_to_key = staticmethod(attr_to_key),
    )
  metacls = type(typename + 'Meta', (SimpleDictMeta,), metaclsattrs)
  # then create a frozen simpledict type from the custom meta type
  frozenbasetype = SimpleFrozenDictType.type(basetype)
  metacls.frozen = metacls(typename, (frozenbasetype,), {})
  # finally create the normal simpledict type from the custom meta type
  return metacls(typename, (basetype,), {})

simpledict.KeyToAttrError = KeyToAttrError
simpledict.KeyToAttrToKeyMismatch = KeyToAttrToKeyMismatch
simpledict.AttrToKeyToAttrMismatch = AttrToKeyToAttrMismatch
