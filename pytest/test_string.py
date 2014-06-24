import pytest

from moretools import camelize, decamelize, isidentifier


def test_camelize():
    for lower_case, CamelCase in [
      ('me', 'Me'),
      ('me_too', 'MeToo'),
      ]:
        assert camelize(lower_case) == CamelCase


def test_decamelize():
    assert decamelize('Me') == 'me'
    assert decamelize('MeToo') == 'me_too'


def test_isidentifier():
    for name in [
      'va_lid',
      '_va_lid',
      'va_lid_',
      'v4l1d',
      ]:
        assert isidentifier(name)

    for name in [
      '1nvalid',
      ]:
        assert not isidentifier(name)
