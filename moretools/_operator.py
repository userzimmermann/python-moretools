__all__ = ['not_']

import operator

from ._tester import Tester, NotTester


def not_(value):
    return not value


def logic_op(logic):
    if isinstance(logic, str):
        name = logic
        logic = getattr(operator, logic)
    else:
        name = logic.__name__

    __all__.append(name)

    testerclass = Tester[logic]

    def op(value, *right):
        if right:
            return logic(value, *right)
        return testerclass(value)

    def not_tester(value):
        return NotTester(testerclass(value))

    setattr(not_, name, not_tester)

    op.__name__ = name
    return op


eq = logic_op('eq')
ne = logic_op('ne')
lt = logic_op('lt')
le = logic_op('le')
gt = logic_op('gt')
ge = logic_op('ge')


def in_(item, seq):
    return item in seq


in_ = logic_op(in_)
contains = logic_op('contains')


from _is import *
