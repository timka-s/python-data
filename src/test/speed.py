#!/usr/bin/env python

""" Comparison of execution speed of the manual and of the generated code. """

from timeit import timeit
from itertools import imap

from ..builder import Native
from ..condition import Is, Field
from .mock_cls import SimpleNamespace as SN

obj = SN(
    id = 2,
    some_set = [
        SN(attr = 3),
        SN(attr = 2) ],
    seq = [1, 2, 3, 4, 5],
    double_set = [
        (1, 2, 3),
        (4, 5, 6) ],
    some_attr = SN(some_var = 234),
    foo = 12345,
    bar = 12345 )

query = Is(
    id__NE = 0,
    some_set__ANY__attr__EQ = 3,
    seq = Is(
      COUNT__LE = 5,
      ALL__IN = range(0, 6) ),
    double_set__ALL__ALL = ~Is(GT = 7),
    some_attr__some_var__LT = 500,
    foo__GE = Field('.bar') )


def test(name, obj, fn):
  print 'Result of %s: %s' % (name, fn(obj))
  print 'Execution time: %s' % timeit(lambda: fn(obj))

generic_fn = Native.makeWhich(query)

def manual_fn(obj):
  return (
        obj.id <> 0
    and any(imap(lambda el: el.attr == 3, obj.some_set))
    and len(obj.seq) <= 5
    and all(imap(lambda el: el in range(0, 6), obj.seq))
    and all(imap(
        lambda el: all(imap(lambda sub_el: not (sub_el > 7), el)),
        obj.double_set ))
    and obj.some_attr.some_var <= 500
    and obj.foo >= obj.bar
  )

print 'Object:'
print obj
print
print 'Query:'
print query
print
print 'Test:'

test('generated function', obj, generic_fn)
test('manual function', obj, manual_fn)




