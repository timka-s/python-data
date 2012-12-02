# -*- coding: utf-8 -*-
from itertools import groupby, chain
from operator import itemgetter

from ._if import If
from ._and import And


class Attr(If):
  attr = property(itemgetter(0))
  content = property(itemgetter(1))

  @classmethod
  def _make(cls, level, data):
    def parse(level, data):
      item = data.next()
      if item[0] == level:
        yield item[1]
      else:
        data = chain((item, ), data)

      level += 1
      data = groupby(data, key = itemgetter(level))

      item = data.next()
      if item[0] == '':
        yield cls._make(level, item[1])
      else:
        data = chain((item,), data)

      for attr, items in data:
        yield cls._create(attr, cls._make(level, items))

    return And._make(parse(level, data))

  def __new__(cls, **kwargs):
    def parse(data):
      for key, value in sorted(data.iteritems(), key = itemgetter(0)):
        path = str(key).split('__')
        yield (len(path) + 1, cls._parse(value)) + tuple(path)

    return cls._make(1, parse(kwargs))

  def __repr__(self):
    return '.%s%s' % (self.attr, self.content)


@If._method
@staticmethod
def __new__(cls, *args, **kwargs):
  def parse():
    if len(args) <> 0:
      yield And(*args)
    if len(kwargs) <> 0:
      yield Attr(**kwargs)

  return And._make(parse())
