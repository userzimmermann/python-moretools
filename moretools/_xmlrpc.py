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

"""moretools._xmlrpc

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['XMLRPCClient', 'XMLRPCMethod']

import re
from warnings import warn

from six.moves.xmlrpc_client import ServerProxy, Fault


class XMLRPCMethod(object):
    """Wrapper for :class:`xmlrpc.client._Method`s
       used by :class:`moretools.XMLRPCClient`.

    - Shoudn't be directly instantiated.
    - Provides __doc__ if server provides 'Method.getdoc'.
    - Shows remote __repr__ if server provides 'Method.__repr__'.
    - Provides :meth:`__dir__` to list all remote sub methods
      from the method namespace if server provides 'system.listMethods'.
    - Returns wrapped sub methods via :meth:`__getattr__`.
    """
    def __init__(self, name, method, client):
        # xmlrpc.client._Method `method` has private __name,
        # so take `name` as extra arg
        self.__name = name
        self.__method = method
        self.__client = client

    def __dir__(self):
        # Find all remote methods starting with this method namespace
        # and return their sub names:
        re_ = re.compile(r'^%s\.(.*)$' % self.__name)
        return [match.group(1)
                for match in map(re_.match, dir(self.__client))
                if match]

    def __getattr__(self, name):
        method = getattr(self.__method, name)
        return XMLRPCMethod(
          '.'.join((self.__name, name)), method, client=self.__client)

    def __call__(self, *args):
        return self.__method(*args)

    @property
    def __doc__(self):
        try:
            # Remote 'Method.getdoc' method must be defined for this to work
            return self.__method.getdoc()
        except Fault:
            return ""

    def __str__(self):
        return self.__name

    def __repr__(self):
        repr_ = type(self).__name__
        try:
            # Remote 'Method.__repr__' method must be defined for this to work
            return repr_ + ': ' + repr(self.__method)
        except Fault:
            return repr_ + ' \'%s\'' % self.__name


class XMLRPCClient(ServerProxy):
    """An extended :class:`xmlrpc.client.ServerProxy`.

    - Provides :meth:`__dir__` to list all remote methods
      if server provides 'system.listMethods'.
    - Returns remote methods via :meth:`__getattr__`
      wrapped with :class:`moretools.XMLRPCMethod`.
    """
    def __dir__(self):
        try:
            return ServerProxy.__getattr__(self, 'system.listMethods')()
        except Fault as e: # Server doesn't provide method
            warn(str(e))
            return []

    def __getattr__(self, name):
        allnames = dir(self)
        if allnames and name not in allnames:
            raise AttributeError(name)
        method = ServerProxy.__getattr__(self, name)
        # `method` has private __name, so pass it as extra arg to wrapper:
        return XMLRPCMethod(name, method, client=self)
