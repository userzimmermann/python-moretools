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

"""functions/classes to get multiple attrs/items from objects at once
returning an iterator in every case
"""

from ._common import *
from ._common import _map

def getattrs(obj, *attrs):
  return _map(partial(getattr, obj), attrs)

class attrsgetter(object):
  __slots__ = 'attrs',

  def __init__(*attrs):
    self.attrs = attrs

  def __call__(obj):
    return getattrs(obj, *self.attrs)

def getitems(obj, *keys):
  return _map(partial(getitem, obj), keys)

class itemsgetter(object):
  __slots__ = 'keys',

  def __init__(*keys):
    self.keys = keys

  def __call__(self, obj):
    return getitems(obj, *self.keys)
