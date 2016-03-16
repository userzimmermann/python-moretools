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

"""moretools._log

Logging helpers.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['logged']

from decorator import decorator

from ._common import *


class LoggedDeco(object):
    """The @logged decorator.

    - Automatically logs function calls as "func.__name__(repr(arg), ...)"
    """
    def __init__(self, logger=None, level=None):
        self.logger = logger
        self.level = level and level.upper()

    def __getitem__(self, logger):
        return type(self)(logger=logger, level=self.level)

    def __getattr__(self, level):
        return type(self)(logger=self.logger, level=level)

    def __call__(self, func, logger=None):
        def logged(func, *args, **kwargs):
            log = getattr(self.logger or logger, self.level.lower())
            logargs = map(repr, args)
            logkwargs = (
              "%s=%s" % (key, repr(value))
              for key, value in kwargs.items())
            log("%s(%s)" % (
              func.__name__, ", ".join(chain(logargs, logkwargs))))
            return func(*args, **kwargs)

        return decorator(logged, func)


logged = LoggedDeco()
