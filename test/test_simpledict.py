"""Test the moretools._simpledict module.

- issimple...dict...class() functions
  are implicitly tested in check_...class() functions.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""

import pytest

from moretools import (
  simpledict, issimpledict, issimpledictclass,
  issimplefrozendict, issimplefrozendictclass,
  issimpledictstruct, issimpledictstructclass,
  )
from moretools._simpledict import (
  SimpleDictType, SimpleFrozenDictType, SimpleDictStructType,
  )


def test_aliases():
    """Test if the simpledict.(...)base class alias attributes
       are correctly assigned.
    """
    assert simpledict.base is SimpleDictType \
      and simpledict.frozenbase is SimpleFrozenDictType \
      and simpledict.structbase is SimpleDictStructType


def check_class(cls, name):
    """Check if simpledict()-created `cls` has correct `name` and bases.
    """
    assert cls.__name__ == name

    # check bases the direct way
    assert issubclass(cls, simpledict.base)
    assert not issubclass(cls, simpledict.frozenbase)
    assert not issubclass(cls, simpledict.structbase)
    # and with the according checker functions (to implicitly test them)
    assert issimpledictclass(cls)
    assert not issimplefrozendictclass(cls)
    assert not issimpledictstructclass(cls)


def check_frozenclass(cls, name):
    """Check if <simpledict class>.frozen `cls` has correct `name` and bases.
    """
    assert cls.__name__ == name + '.frozen'

    # check bases the direct way
    assert issubclass(cls, simpledict.base)
    assert issubclass(cls, simpledict.frozenbase)
    assert not issubclass(cls, simpledict.structbase)
    # and with the according checker functions (to implicitly test them)
    assert issimpledictclass(cls)
    assert issimplefrozendictclass(cls)
    assert not issimpledictstructclass(cls)


def check_structclass(cls, name):
    """Check if <simpledict class>.struct `cls` has correct `name`, bases
       and slots.
    """
    assert cls.__name__ == name + '.struct'

    # check bases the direct way
    assert issubclass(cls, simpledict.base)
    assert not issubclass(cls, simpledict.frozenbase)
    assert issubclass(cls, simpledict.structbase)
    # and with the according checker functions (to implicitly test them)
    assert issimpledictclass(cls)
    assert not issimplefrozendictclass(cls)
    assert issimpledictstructclass(cls)

    assert cls.__slots__ == ['__name__', '__bases__']


def test_simpledict():
    """Test simpledict() class creation and usage.
    """
    SD = simpledict('SD')
    check_class(SD, 'SD')
    check_frozenclass(SD.frozen, 'SD')
    check_structclass(SD.struct, 'SD')

    SD = simpledict('SD', frozenbase=None)
    assert not hasattr(SD, 'frozen')
    check_class(SD, 'SD')
    check_structclass(SD.struct, 'SD')

    SD = simpledict('SD', structbase=None)
    assert not hasattr(SD, 'struct')
    check_class(SD, 'SD')
    check_frozenclass(SD.frozen, 'SD')

    SD = simpledict('SD', frozenbase=None, structbase=None)
    assert not hasattr(SD, 'frozen')
    assert not hasattr(SD, 'struct')
    check_class(SD, 'SD')
