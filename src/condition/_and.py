# -*- coding: utf-8 -*-
from heapq import merge
from operator import itemgetter

from ._if import If


@If._type('and')
class And(If):
  content = property(itemgetter(0))

  @classmethod
  def _make(cls, data):
    data = (item.content if isinstance(item, cls) else (item,) for item in data)
    data = tuple(merge(*data))

    if len(data) == 0:
      return cls._type_empty()
    elif len(data) == 1:
      return data[0]
    else:
      return cls._new(data)

  def __new__(cls, *args):
    return cls._make(cls._parse(item) for item in args)

  def __repr__(self):
    return '(%s)' % (' && '.join(str(item) for item in self.content))
