from six import with_metaclass

__all__ = ['Tester', 'NotTester']


class Meta(type):
    def __getitem__(cls, logic):
        class tester(cls):
            pass

        tester.logic = staticmethod(logic)
        return tester


class Tester(with_metaclass(Meta, object)):
    def __init__(self, *args):
        self.args = args

    def __call__(self, value):
        return self.logic(value, *self.args)

    def __eq__(self, value):
        return self(value)

    def __ne__(self, value):
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
