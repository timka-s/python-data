#!/usr/bin/env python

from timeit import timeit

from ...builder import Native
from ...condition import If, Field
from ..mock_cls import SimpleNamespace as SN


def _print(key):
  print (key +  ' = ' + str(globals()[key]))
  print


obj = SN(
    id = 2,
    some_set = [
      SN(attr = 3),
      SN(attr = 2)
    ],
    seq = [1, 2, 3, 4, 5],
    double_set = [
      (1, 2, 3),
      (4, 5, 6)
    ],
    some_attr = SN(
      some_var = 234
    ),
    foo = 12345,
    bar = 12345
)
_print('obj')


query = If(
    id__NE = 0,
    some_set__ANY__attr__EQ = 3,
    seq__COUNT__LE = 5,
    seq__ALL__IN = range(0, 6),
    double_set__ALL__ALL = ~If(GT = 7),
    some_attr__some_var__LT = 500,
    foo__GE = Field('.bar'),
)
_print('query')


comparision = Native.make(query)

def comparision_code(obj):
  return (
        obj.id <> 0
    and any(map(lambda el: el.attr == 3, obj.some_set))
    and len(obj.seq) <= 5
    and all(map(lambda el: el in range(0, 6), obj.seq))
    and all(map(
        lambda el: all(map(lambda sub_el: not (sub_el > 7), el)),
        obj.double_set))
    and obj.some_attr.some_var <= 500
    and obj.foo >= obj.bar
  )


res = comparision(obj)
_print('res')
print timeit(lambda: comparision(obj))


res_code = comparision_code(obj)
_print('res_code')
print timeit(lambda: comparision_code(obj))
