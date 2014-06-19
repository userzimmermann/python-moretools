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

"""moretools._cached

The @cached decorator.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['cached']

from inspect import getargspec

from ._common import *


def cached(func):
    argspec = getargspec(func)
    if not argspec.keywords:
        nargs = len(argspec.args)
        varargs = argspec.varargs
        if not nargs and not varargs:
            def cached(func):
                try:
                    return wrapper.result
                except AttributeError:
                    result = wrapper.result = func()
                    return result

            wrapper = decorator(cached, func)
            return wrapper

        if nargs == 1 and not varargs:
            def cached(func, arg):
                try:
                    return wrapper.results[arg]
                except KeyError:
                    result = wrapper.results[arg] = func(arg)
                    return result
        else:
            def cached(func, *args):
                try:
                    return wrapper.results[args]
                except KeyError:
                    result = wrapper.results[args] = func(*args)
                    return result
    else:
        def cached(func, *args, **kwargs):
            key = args, frozenset(kwargs.items())
            try:
                return wrapper.results[key]
            except KeyError:
                result = wrapper.results[key] = func(*args, **kwargs)
                return result

    wrapper = decorator(cached, func)
    wrapper.results = {}
    return wrapper
