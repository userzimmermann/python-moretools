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

"""Wrapper classes for use in `filterattrs'/`filteritems'
   for testing other relations between attrs/keys and values than equality.
"""

from ._common import *
from ._common import _zip


class _query(object):
    __slots__ = ['args']

    def __init__(self, *args):
        self.args = args

    def __eq__(self, value):
        return all(starmap(self._eq, _zip(repeat(value), self.args)))


class qeq(_query):
    def _eq(self, value, arg):
        return value == arg


class qlt(_query):
    def _eq(self, value, arg):
        return value < arg


class qle(_query):
    def _eq(self, value, arg):
        return value <= arg


class qin(_query):
    def _eq(self, value, arg):
        return value in arg


class qcontains(_query):
    def _eq(self, value, arg):
        return arg in value


class qand(qeq):
  pass


class qor(qeq):
  def __eq__(self, value):
    return any(starmap(self._eq, _zip(repeat(value), self.args)))


class _kwquery(_query):
    __slots__ = ['kwargs']

    def __init__(self, *args, **kwargs):
        _query.__init__(self, *args)
        self.kwargs = kwargs

    def __eq__(self, value):
        return _query.__eq__(self, value) and all(starmap(
          lambda value, key_and_value: self._kweq(value, *key_and_value),
          _zip(repeat(value), self.kwargs.items())))


class qattrs(_kwquery):
    def _eq(self, value, arg):
        return hasattr(value, arg)

    def _kweq(self, value, key, kvalue):
        return getattr(value, key) == kvalue
