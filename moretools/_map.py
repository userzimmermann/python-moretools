# python-moretools
#
# many more basic tools for python 2/3
# extending itertools, functools and operator
#
# Copyright (C) 2011-2013 Stefan Zimmermann <zimmermann.code@gmail.com>
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

"""functions for mapping sequence elements to their attrs/items or calls
"""

from ._common import *
from ._common import _map


def mapattr(seq, attr):
    return _map(lambda item: getattr(item, attr), seq)

def mapmapattr(seqs, attr):
    return _map(lambda seq: mapattr(seq, attr), seqs)

def mapattrs(seq, *attrs):
    return _map(lambda item: _map(partial(getattr, item), attrs), seq)

def mapmapattrs(seqs, *attrs):
    return _map(lambda seq: mapattrs(seq, *attrs), seqs)


def mapitem(seq, key):
    return _map(lambda item: item[key], seq)

def mapmapitem(seqs, key):
    return _map(lambda seq: mapitem(seq, keys), seqs)

def mapitems(seq, *keys):
    return _map(lambda item: _map(partial(getitem, item), keys), seq)

def mapmapitems(seqs, *keys):
    return _map(lambda seq: mapitems(seq, *keys), seqs)


def mapcall(seq, *args, **kwargs):
    return _map(lambda item: item(*args, **kwargs), seq)

def mapmapcall(seqs, *args, **kwargs):
    return _map(lambda seq: mapcall(seq, *args, **kwargs), seqs)

def mapmethodcall(seq, name, *args, **kwargs):
    return mapcall(map(attrgetter(name), seq), *args, **kwargs)

def mapmapmethodcall(seqs, name, *args, **kwargs):
    return _map(lambda seq: mapmethodcall(seq, name, *args, **kwargs), seqs)


def mapjoin(seqs, sep=''):
    return _map(sep.join, seqs)
