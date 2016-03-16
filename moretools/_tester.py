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

"""moretools._tester


.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = ['Tester', 'NotTester']


class Meta(type):
    """Metaclass for :class:`moretools.Tester`

    - Allows creating Tester subclasses for certain logic functions
      via Tester[<logic>]
    """
    def __getitem__(cls, logic):
        class tester(cls):
            pass

        tester.logic = staticmethod(logic)
        return tester


class Tester(with_metaclass(Meta, object)):
    """Base class for creating logical value testers.

    - Create subclass with associated logic function via Tester[<logic>]
    - Instantiate Tester with right hand logic function args.
    - Test value using <Tester instance>(value)
      or <Tester instance> == value,
      which calls <logic>(value, *<right hand args>),
      (which should return True or False),
      or negatively test it using <Tester instance> != value
    """
    def __init__(self, *args):
        """Instantiate Tester using `args` as right hand args
           for calling the logic function.
        """
        self.args = args

    def __call__(self, value):
        """Test `value`.
        """
        return self.logic(value, *self.args)

    def __eq__(self, value):
        """Test `value`.
        """
        return self(value)

    def __ne__(self, value):
        """Negatively test `value`.
        """
        return not self(value)

    def and_(self, tester):
        return AndTester(self, tester)

    def __and__(self, tester):
        return self.and_(tester)

    def or_(self, tester):
        return OrTester(self, tester)

    def __or__(self, tester):
        return self.or_(tester)

    def xor(self, tester):
        return XorTester(self, tester)

    def __xor__(self, tester):
        return self.xor(tester)


class NotTester(Tester):
    def __init__(self, tester):
        self.tester = tester

    def __call__(self, value):
        return not self.tester(value)


class AndTester(Tester):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, value):
        return self.left(value) & self.right(value)


class OrTester(Tester):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, value):
        return self.left(value) | self.right(value)


class XorTester(Tester):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, value):
        return self.left(value) ^ self.right(value)


class AttrTester(Tester):
    def __init__(self, attr, tester):
        self.attr = attr
        self.tester = tester

    def __call__(self, value):
        value = getattr(value, self.attr)
        return self.tester(value)


class KeyTester(Tester):
    def __init__(self, key, tester):
        self.key = key
        self.tester = tester

    def __call__(self, value):
        value = value[self.key]
        return self.tester(value)
