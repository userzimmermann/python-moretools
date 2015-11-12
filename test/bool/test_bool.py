"""
Test moretools for creating custom bool classes.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""

from moretools import StrictBool, StrictBoolMeta, strictbool, \
    isboolclass, isbool

import pytest


class TestStrictBool(object):
    """Test abstract :class:`moretools.StrictBool`.
    """
    def test_class(self):
        assert type(StrictBool) is StrictBoolMeta
        assert issubclass(StrictBool, int)

    def test_abstract(self):
        # check that abstract class can't be instantiated
        with pytest.raises(TypeError) as exc:
            StrictBool(True)
        assert "abstract" in str(exc.value)

    def test_init(self, strictboolclass, true_values, false_values,
                  invalid_values):
        # check that all defined true and false init values work correctly
        for value in [True] + true_values:
            obj = strictboolclass(value)
            assert obj is True
        for value in [False] + false_values:
            obj = strictboolclass(value)
            assert obj is False
        # and that using other values raises an error
        for value in invalid_values:
            with pytest.raises(ValueError):
                strictboolclass(value)


def test_strictbool_attrs(true_values, false_values):
    """Check extra attributes of :func:`moretools.strictbool`.
    """
    assert strictbool.base is StrictBool


def test_strictbool(true_values, false_values):
    """Test :func:`moretools.strictbool` class creator.
    """
    boolclass = strictbool('Bool', true=true_values, false=false_values)
    assert boolclass.__name__ == 'Bool'
    assert boolclass is not StrictBool
    assert issubclass(boolclass, StrictBool)
    assert type(boolclass) is not StrictBoolMeta
    assert issubclass(type(boolclass), StrictBoolMeta)
    assert boolclass.true == type(boolclass).true == true_values
    assert boolclass.false == type(boolclass).false == false_values


def test_strictbool_without_true_false(true_values, false_values):
    """Test :func:`moretools.strictbool` class creator
       without passing ``true=`` and ``false=`` value lists.
    """
    boolclass = strictbool('Bool')
    assert boolclass.true is type(boolclass).true is None
    assert boolclass.false is type(boolclass).false is None
    assert boolclass(True) is True
    assert boolclass(False) is False
    for value in true_values + false_values:
        with pytest.raises(ValueError):
            boolclass(value)


def test_strictbool_with_custom_base():
    """Test :func:`moretools.strictbool` class creator
       with a custom intermediate :class:`moretools.StrictBool`-derived
       ``base=`` class argument.
    """
    with pytest.raises(TypeError):
        strictbool('Bool', base=bool)

    class Bool(StrictBool):
        pass

    boolclass = strictbool('Bool', base=Bool)
    assert boolclass is not Bool
    assert issubclass(boolclass, Bool)


def test_isboolclass(strictboolclass, strictboolobj):
    """Test :func:`moretools.isboolclass` check.
    """
    # first make sure that strictboolobj fixture
    # is really a StrictBool instance
    # (no common use case, as StrictBool.__new__
    # normally returns builint bools)
    assert not isinstance(strictboolobj, bool)
    # then perform actual tests
    for class_ in bool, StrictBool, strictboolclass:
        assert isboolclass(class_)
    for class_ in object, int:
        assert not isboolclass(class_)
    for obj in object(), False, 1, 'True', 'bool', strictboolobj:
        with pytest.raises(TypeError) as exc:
            isboolclass(obj)
        assert str(exc.value) == "isboolclass() arg must be a class"


def test_isbool(strictboolobj):
    """Test :func:`moretools.isbool` instance check.
    """
    # first make sure that strictboolobj fixture
    # is really a StrictBool instance
    # (no common use case, as StrictBool.__new__
    # normally returns builint bools)
    assert not isinstance(strictboolobj, bool)
    # then perform actual tests
    for obj in True, False, strictboolobj:
        assert isbool(obj)
    for obj in object, object(), 1, 'False', [True], {False}:
        assert not isbool(obj)
