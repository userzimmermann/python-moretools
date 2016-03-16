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

"""moretools._pop

Functions for popping attributes and items from objects.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['popattr', 'popitem']

from ._common import *
from ._undefined import undefined


def popattr(obj, name, default=undefined):
    """Pops the `name`d attribute from `obj`
       by calling getattr() and delattr(),
       returning its value.

    - If the attribute doesn't exist and `default` is given,
      that value will be returned instead
      (otherwise an AttributeError is raised).
    """
    try:
        value = getattr(obj, name)
    except AttributeError:
        if default is undefined:
            raise
        return default

    delattr(obj, name)
    return value


def popitem(obj, key, default=undefined):
    """Pops the item`name`d attribute from `obj`
       by calling getattr() and delattr(),
       returning its value.

    - If the attribute doesn't exist and `default` is given,
      that value will be returned instead
      (otherwise the exception is re-raised).
    """
    try:
        value = obj[key]
    except (KeyError, IndexError):
        if default is undefined:
            raise
        return default

    del obj[key]
    return value
