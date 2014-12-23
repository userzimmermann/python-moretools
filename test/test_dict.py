"""Test the moretools._dict module.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""

import pytest

from collections import OrderedDict
from operator import is_

from moretools import (
  dictkeys, dictvalues, dictitems, dictfilter,
  iterkeys, itervalues, iteritems)


def test_aliases():
    """Just test that six-like iter... aliases for dict... functions
       are correctly assigned.
    """
    assert iterkeys is dictkeys and itervalues is dictvalues \
      and iteritems is dictitems


# the reference dictionaries to test functions with
ORDERED_DICT = OrderedDict([
  ('one', [2]),
  (3, ('f', 'o', 'u', 'r')),
  (5.6, 7),
  (('eight', 9), {10}),
  ])
DICT = dict(ORDERED_DICT)


def test_dictkeys():
    """Test the dictkeys() function,
       which returns an iterator of a dictionary's keys
       and also works with simpledict() class instances.
    """
    for d in [DICT, ORDERED_DICT]:
        keys = dictkeys(d)
        # dictkeys() should not return lists, only iterators
        assert not isinstance(keys, list)
        # compare with reference sequence from dict method
        assert all(map(is_, keys, d.keys()))
        # and check that iterator is exhausted
        with pytest.raises(StopIteration):
            next(keys)


def test_dictvalues():
    """Test the dictvalues() function,
       which returns an iterator of a dictionary's values
       and also works with simpledict() class instances.
    """
    for d in [DICT, ORDERED_DICT]:
        values = dictvalues(d)
        # dictvalues() should not return lists, only iterators
        assert not isinstance(values, list)
        # compare with reference sequence from dict method
        assert all(map(is_, values, d.values()))
        # and check that iterator is exhausted
        with pytest.raises(StopIteration):
            next(values)


def test_dictitems():
    """Test the dictitems() function,
       which returns an iterator of a dictionary's (key, value) pairs
       and also works with simpledict() class instances.
    """
    for d in [DICT, ORDERED_DICT]:
        items = dictitems(d)
        # dictitems() should not return lists, only iterators
        assert not isinstance(items, list)
        # compare with reference sequence from dict method
        for (key, value), (refkey, refvalue) in zip(items, d.items()):
            assert key is refkey and refvalue is refvalue
        # and check that iterator is exhausted
        with pytest.raises(StopIteration):
            next(items)
