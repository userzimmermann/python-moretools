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

from ._common import *
from ._simpledict import SimpleDictType

from six.moves import UserString, UserList, UserDict


number_types = integer_types + (float, complex)

string_types = (string_types) + (UserString,)

list_types = (list, UserList)

dict_types = (dict, UserDict, SimpleDictType)


def isintclass(cls):
    return issubclass(cls, int)

isinttype = isintclass

def isint(value):
    return isinstance(value, int)


if PY2:
    def islongclass(cls):
        return issubclass(cls, long)

    islongtype = islongclass

    def islong(value):
        return isinstance(value, long)


def isintegerclass(cls):
    return issubclass(cls, integer_types)

isintegertype = isintegerclass

def isinteger(value):
    return isinstance(value, integer_types)


def isfloatclass(cls):
    return issubclass(cls, float)

isfloattype = isfloatclass

def isfloat(value):
    return isinstance(value, float)


def iscomplexclass(cls):
    return issubclass(cls, complex)

iscomplextype = iscomplexclass

def iscomplex(value):
    return isinstance(value, complex)


def isnumberclass(cls):
    return issubclass(cls, number_types)

isnumbertype = isnumberclass

def isnumber(value):
    return isinstance(value, number_types)


def isstringclass(cls):
    return issubclass(cls, string_types)

isstringtype = isstringclass

def isstring(value):
    return isinstance(value, string_types)


def istupleclass(cls):
    return issubclass(cls, tuple)

istupletype = istupleclass

def istuple(value):
    return isinstance(value, tuple)


def islistclass(cls):
    return issubclass(cls, list_types)

islisttype = islistclass

def islist(value):
    return isinstance(value, list_types)


def issetclass(cls):
    return issubclass(cls, set)

issettype = issetclass

def isset(value):
    return isinstance(value, set)


def isdictclass(cls):
    return issubclass(cls, dict_types)

isdicttype = isdictclass

def isdict(value):
    return isinstance(value, dict_types)
