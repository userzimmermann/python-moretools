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

class SimpleDictType(object):
  """A simple *mapping* type providing item value access
  with `__getattr__`/`__setattr__`
  using custom *key*<-->*attrname* conversion functions.

  * Don't instantiate this class directly,
  use the `simpledict` function to create a customized derived class
  * Attribute name representations of mapping keys
  must **not** start with an *underscore*.
  * Automatically checks for valid *key*<-->*attrname* conversions
  on item insertion.
  * Doesn't provide any **non**-*special methods*.
  * `.__iter__()` returns an items (key/value pairs) iterator.
  """
  _re_attrname = _re.compile('^[A-Za-z][A-Za-z0-9_]*$')

  def __init__(self, mapping = (), **items):
    """Instantiate the SimpleDictType with optional initial values.
    """
    self._dict = self._dicttype(mapping, **items)
    for key in self._dict.keys():
      attrname = self._key_to_attr(key)
      # check attribute name validity
      # *raises* `KeyToAttrError`
      self._check_attr(key, attrname)
      # check reverse attr-->key conversion
      # *raises* `KeyToAttrToKeyMismatch`
      self._reverse_check_key(key, attrname)

  def _check_attr(self, key, attrname):
    if not self._re_attrname.match(attrname):
      if attrname.startswith('_'):
        raise KeyToAttrError(
          'Attribute names must not start with an underscore',
          key, attrname)
      raise KeyToAttrError(
        'Invalid Python identifier', key, attrname)

  def _reverse_check_key(self, key, attrname):
    """Check reverse attr-->key conversion.
    """
    key_from_attr = self._attr_to_key(attrname)
    if key_from_attr != key:
      raise KeyToAttrToKeyMismatch(key, attrname, key_from_attr)

  def _reverse_check_attr(self, attrname, key):
    """Check reverse key-->attr conversion.
    """
    attr_from_key = self._key_to_attr(key)
    if attr_from_key != attrname:
      raise AttrToKeyToAttrMismatch(attrname, key, attr_from_key)

  def __getattr__(self, name):
    try:
      key = self._attr_to_key(name)
      return self._dict[key]
    except KeyError:
      raise AttributeError(name)

  def __setattr__(self, name, value):
    if name.startswith('_'): # is real (internal) attribute?
      object.__setattr__(self, name, value)
    else: # convert name to key and store in `self._dict`
      key = self._attr_to_key(name)
      # check reverse key-->attr conversion
      # *raises* `AttrToKeyToAttrMismatch`
      self._reverse_check_attr(name, key)
      # accept name/value pair
      self._dict[key] = value

  def __delattr__(self, name):
    if name.startswith('_'): # is real (internal) attribute?
      raise AttributeError(name)
    key = self._attr_to_key(name)
    del self._dict[key]

  def __dir__(self):
    return [self._key_to_attr(key) for key in self._dict.keys()]

  def __iter__(self):
    return iter(self._dict.items())

  def __len__(self):
    return len(self._dict)

  def __setitem__(self, key, value):
    attrname = str(self._key_to_attr(key))
    # check attribute name validity
    # *raises* `KeyToAttrError`
    self._check_attr(key, attrname)
    # check reverse attr-->key conversion
    # *raises* `KeyToAttrToKeyMismatch`
    self._reverse_check_key(key, attrname)
    # accept the key/value pair
    self._dict[key] = value

  def __getitem__(self, key):
    return self._dict[key]

  def __delitem__(self, key):
    del self._dict[key]

  def __repr__(self):
    return 'simpledict(%s)' % repr(self._dict)

def simpledict(
  name, dicttype = dict,
  key_to_attr = lambda key: key, attr_to_key = lambda name: name
  ):
  """Create a custom :class:`SimpleDictType`-derived type.

  :param dicttype: The *mapping* type used for internal *item* storage.
  :param key_to_attr: The *function*
  used for items' *key*-->*attrname* conversions.
  :param attr_to_key: The *function*
  used for items' *attrname*-->*key* conversions.
  """
  attrs = dict(
    _dicttype = dicttype,
    _key_to_attr = staticmethod(key_to_attr),
    _attr_to_key = staticmethod(attr_to_key),
    )
  return type(name, (SimpleDictType,), attrs)

simpledict.KeyToAttrError = KeyToAttrError
simpledict.KeyToAttrToKeyMismatch = KeyToAttrToKeyMismatch
simpledict.AttrToKeyToAttrMismatch = AttrToKeyToAttrMismatch
