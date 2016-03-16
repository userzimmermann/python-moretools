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

"""moretools._string

Several string manipulation/converter functions.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['camelize', 'decamelize', 'isidentifier']

import re as _re

from ._common import *


def camelize(string, sep='', joiner=''):
    """Convert a *lower_case* `string` to a *CamelCase* string.

    - Capitalizes after any non-alphanumerical or explicit `sep` string.
    - Also capitalizes after numbers.
    """
    if not string:
        return ''
    slen = len(string)
    return _re.sub(
      r'(%s|([0-9]+))([a-z]?)' % (sep or r'[^A-Za-z0-9]'),
      lambda match: (
        (match.group(2) or '') # numbers
        + ((match.group(3) or match.end() != slen) and joiner or '')
        + (match.group(3) or '').upper()
        ),
      string[0].upper() + string[1:]) #.capitalize())


def decamelize(string, joiner='_'):
    """Convert a *CamelCase* `string` to a *lower_case* string.

    - The underscores can be changed to a custom `joiner` string.
    """
    def replace(match):
        prefix = ( # Don't prepend the joiner to the beginning of string
          '' if match.group(2) else joiner
          )
        caps = match.group(1).lower()
        follower = match.group(3)
        if not follower:
            return prefix + caps
        if len(caps) == 1:
            return prefix + caps + follower
        return prefix + caps[:-1] + joiner + caps[-1] + follower

    return _re.sub('((^[A-Z]+)|[A-Z]+)([a-z])?', replace, string)


_re_identifier = _re.compile('^[A-Za-z_][A-Za-z0-9_]*$')

def isidentifier(string):
    """Test if a `string` is a valid Python identifier.
    """
    return bool(_re_identifier.match(string))
