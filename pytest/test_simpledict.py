import pytest

from moretools import simpledict


def test_simpledict():
    SD = simpledict('SD')

    for cls in SD, SD.frozen, SD.struct:
        assert issubclass(cls, simpledict.base)
    assert issubclass(SD.frozen, simpledict.frozenbase)
    assert issubclass(SD.struct, simpledict.structbase)

    assert SD.struct.__slots__ == ['__name__', '__bases__']

    SD = simpledict('SD', frozenbase=None)
    assert not hasattr(SD, 'frozen')

    SD = simpledict('SD', structbase=None)
    assert not hasattr(SD, 'struct')
