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

"""Common imports of standard itertools, functools and operators
   and Python 2/3 unifications.
"""
from six import *

from operator import *
from itertools import *
from functools import *
from collections import *
## from decorator import *


if PY2: # always use the iterator variants of the following standard tools
    _map = imap
    _filter = ifilter
    _filterfalse = ifilterfalse
    _zip = izip
else:
    _map = map
    _filter = filter
    _filterfalse = filterfalse
    _zip = zip
