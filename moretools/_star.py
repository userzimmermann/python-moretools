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

"""Star versions of standard itertools (like starmap).
"""

from ._common import *
from ._common import _filter, _filterfalse


def startakewhile(fun, seqs):
    return takewhile(lambda seq: fun(*seq), seqs)


def stardropwhile(fun, seqs):
    return dropwhile(lambda seq: fun(*seq), seqs)


def starreduce(fun, seqs, initial):
    return reduce(lambda result, seq: fun(result, *seq), seqs, initial)


def starresultsreduce(fun, seq, initial):
    return reduce(
      lambda resultseq, item: fun(*chain(resultseq, (item,))),
      seq, initial)


def starresultsstarreduce(fun, seqs, initial):
    return reduce(
      lambda resultseq, seq: fun(*chain(resultseq, seq)),
      seq, initial)


def starfilter(fun, seq):
    return _filter(lambda item: fun(*item), seq)


def starfilterfalse(fun, seq):
    return _filterfalse(lambda item: fun(*item), seq)
