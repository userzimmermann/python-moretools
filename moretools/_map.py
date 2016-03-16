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

"""moretools._map

[Deprecated] Functions for mapping sequence elements
or elements of sequences of sequences to their attrs, items or calls.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six.moves import map

from ._get import getitem


def mapmapattr(seqs, attr):
    return map(lambda seq: mapattr(seq, attr), seqs)

def mapattrs(seq, *attrs):
    return map(lambda item: map(partial(getattr, item), attrs), seq)

def mapmapattrs(seqs, *attrs):
    return map(lambda seq: mapattrs(seq, *attrs), seqs)


def mapmapitem(seqs, key):
    return map(lambda seq: mapitem(seq, keys), seqs)

def mapitems(seq, *keys):
    return map(lambda item: map(partial(getitem, item), keys), seq)

def mapmapitems(seqs, *keys):
    return map(lambda seq: mapitems(seq, *keys), seqs)


def mapmapcall(seqs, *args, **kwargs):
    return map(lambda seq: mapcall(seq, *args, **kwargs), seqs)

def mapmethodcall(seq, name, *args, **kwargs):
    return mapcall(map(attrgetter(name), seq), *args, **kwargs)

def mapmapmethodcall(seqs, name, *args, **kwargs):
    return map(lambda seq: mapmethodcall(seq, name, *args, **kwargs), seqs)


def mapjoin(seqs, sep=''):
    return map(sep.join, seqs)
