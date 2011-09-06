# python-moretools
#
# many more basic tools for python 2/3
# extending itertools, functools and operator
#
# Copyright (C) 2011 Stefan Zimmermann <zimmermann.code@googlemail.com>
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

"""functions for filtering sequence elements by attr/item checking
"""

from ._common import *
from ._common import _map, _filter

def filterattrs(seq, *attrs, **attrs_and_values):
  return _filter(
    lambda seqitem: all(chain(
      _map(partial(hasattr, seqitem), attrs),
      starmap(lambda attr, value: getattr(seqitem, attr) == value,
              attrs_and_values.items()))),
    seq)

def filteritems(seq, **keys_and_values):
  return _filter(
    lambda seqitem: all(chain(
      _map(partial(hasitem, seqitem), keys),
      starmap(lambda key, value: seqitem[key] == value,
              keys_and_values.items()))),
    seq)

## def filterkeys(, **keys_and_values):
