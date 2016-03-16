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

"""moretools._collections

[Deprecated] Functions to create varius collections of collections
from sequences containing only sequences.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six.moves import map


def tupleoftuples(self, seqs):
    return tuple(map(tuple, seqs))

def tupleoflists(self, seqs):
    return tuple(map(list, seqs))

def tupleofsets(self, seqs):
    return tuple(map(set, seqs))

def tupleofdicts(self, seqs):
    return list(map(dict, seqs))


def listoftuples(self, seqs):
    return list(map(tuple, seqs))

def listoflists(self, seqs):
    return list(map(list, seqs))

def listofsets(self, seqs):
    return list(map(set, seqs))

def listofdicts(self, seqs):
    return list(map(dict, seqs))


def setoftuples(self, seqs):
    return set(map(tuple, seqs))
