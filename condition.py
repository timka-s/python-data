# -*- coding: utf-8 -*-
from heapq import merge
from itertools import groupby, chain
from operator import itemgetter


class If(tuple):
  @classmethod
  def _new(cls, *args):
    return tuple.__new__(cls, args)

  @classmethod
  def _parse(cls, data):
    if isinstance(data, If):
      return data
    elif isinstance(data, dict):
      return IfAttr(**data)
    elif isinstance(data, (tuple, list, set)):
      return IfOr(*data)
    else:
      return IfValue(data)

  def __new__(cls, *args, **kwargs):
    def parse():
      if len(args) <> 0:
        yield IfAnd(*args)
      if len(kwargs) <> 0:
        yield IfAttr(**kwargs)

    return IfAnd._make(parse())

  def __xor__(self, other):
    other = type(self)._parse(other)
    return ((self & ~other) | (~self & other))

  def __add__(self, other):
    return (self | other)

  def __sub__(self, other):
    other = type(self)._parse(other)
    return (self & ~other)


class IfEmpty(If):
  def __new__(cls):
    return cls._instance

  def __repr__(self):
    return 'is NOTHING'
IfEmpty._instance = IfEmpty._new()


class IfValue(If):
  content = property(itemgetter(0))

  def __new__(cls, data):
    return cls._new(data)

  def __repr__(self):
    return '=`%s`' % str(self.content)


class IfField(If):
  source = property(itemgetter(0))
  depth = property(itemgetter(1))
  path = property(itemgetter(2))

  def __new__(cls, src):
    outer = src.lstrip('.')
    return cls._new(src, len(src) - len(outer), outer.split('__'))

  def __repr__(self):
    return '=%s' % str(self.source)


class IfNot(If):
  content = property(itemgetter(0))

  @classmethod
  def _make(cls, data):
    if isinstance(data, cls):
      return data.content
    else:
      return cls._new(data)

  def __new__(cls, data):
    return cls._make(cls._parse(data))

  def __repr__(self):
    return '~%s' % str(self.content)
If.__invert__ = lambda self: IfNot._make(self)


class IfAnd(If):
  content = property(itemgetter(0))

  @classmethod
  def _make(cls, data):
    data = (item.content if isinstance(item, cls) else (item,) for item in data)
    data = tuple(merge(*data))

    if len(data) == 0:
      return IfEmpty()
    elif len(data) == 1:
      return data[0]
    else:
      return cls._new(data)

  def __new__(cls, *args):
    return cls._make(cls._parse(item) for item in args)

  def __repr__(self):
    return '(%s)' % (' && '.join(str(item) for item in self.content))
If.__and__ = lambda self, other: IfAnd(self, other)


class IfOr(If):
  content = property(itemgetter(0))

  _make = IfAnd._make
  __new__ = IfAnd.__new__

  def __repr__(self):
    return '(%s)' % (' || '.join(str(item) for item in self.content))
If.__or__ = lambda self, other: IfOr(self, other)


class IfAttr(If):
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
        yield cls._from_items(level, item[1])
      else:
        data = chain((item,), data)

      for attr, items in data:
        yield cls._new(attr, cls._make(level, items))

    return IfAnd._make(parse(level, data))

  def __new__(cls, **kwargs):
    def parse(data):
      for key, value in sorted(data.iteritems(), key = itemgetter(0)):
        path = str(key).split('__')
        yield (len(path) + 1, cls._parse(value)) + tuple(path)

    return cls._make(1, parse(kwargs))

  def __repr__(self):
    return '.%s%s' % (self.attr, self.content)
