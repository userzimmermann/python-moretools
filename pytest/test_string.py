"""Test the moretools._string module.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""

import pytest

from moretools import camelize, decamelize, isidentifier


CAMELIZED = {
  'me': 'Me',
  'me_too': 'MeToo',
  }.items()


def test_camelize():
    """Test the string camelize() function.
    """
    for lower_case, CamelCase in CAMELIZED:
        assert camelize(lower_case) == CamelCase


def test_decamelize():
    """Test the string decamelize() function.
    """
    for lower_case, CamelCase in CAMELIZED:
        assert decamelize(CamelCase) == lower_case


def test_isidentifier():
    """Test the isidentifier() function,
       which checks if a string contains a valid Python identifier.
    """
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
