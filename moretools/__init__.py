# python-moretools
#
# many more basic tools for python 2/3
# extending itertools, functools and operator
#
# Copyright (C) 2011-2014 Stefan Zimmermann <zimmermann.code@gmail.com>
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

"""Many more basic tools for Python 2/3
   extending itertools, functools and operator.
"""

from zetup import find_zetup_config


zfg = find_zetup_config(__name__)

__distribution__ = zfg.DISTRIBUTION.find(__path__[0])
__description__ = zfg.DESCRIPTION

__version__ = zfg.VERSION

__requires__ = zfg.REQUIRES.checked


from ._map import *
from ._repeat import *
from ._star import *
from ._empty import *
from ._filter import *
from ._query import *
from ._caller import *
from ._get import *
from ._set import *
from ._has import *
from ._del import *
from ._bool import *
from ._collections import *
from ._simpledict import *
from ._multi import *
from ._string import *
from ._multidict import *
from ._multisimpledict import *
from ._lazy import *
from ._cached import *
from ._log import *
from ._xmlrpc import *
from ._types import *
from ._operator import *
