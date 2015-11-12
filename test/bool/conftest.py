"""
Fixtures for testing moretools for creating custom bool classes.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""

from moretools import StrictBool

import pytest


@pytest.fixture
def true_values():
    """True values to be used for a :class:`StrictBool`-derived class.
    """
    return [1, 'true', 'yes']


@pytest.fixture
def false_values():
    """False values to be used for a :class:`StrictBool`-derived class.
    """
    return [0, 'false', 'no']


@pytest.fixture
def invalid_values():
    """Some values not matching any items from
       ``true_values`` or ``false_values`` fixtures.
    """
    return [2, 'on', 'off']


@pytest.fixture
def strictboolclass(true_values, false_values):
    """A sample :class:`StrictBool`-derived class.
    """
    class Bool(StrictBool):
        true = true_values
        false = false_values

    return Bool


@pytest.fixture
def strictboolobj(true_values, false_values):
    """A real :class:`StrictBool`-derived instance.
    """
    class Bool(StrictBool):
        true = true_values
        false = false_values

        def __new__(cls, value):
            # avoid creation of builtin bool
            # and create real Bool instance instead
            return super(StrictBool, cls).__new__(
                cls, StrictBool.__new__(cls, value))

    return Bool(True)
