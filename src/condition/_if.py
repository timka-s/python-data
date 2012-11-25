# -*- coding: utf-8 -*-


class IfMeta(type):
  def __init__(cls, name, bases, dct):
    if name <> 'If':
      attr_name = '_' + cls.__name__

      if hasattr(If, '_' + cls.__name__):
        raise TypeError('SubType with the same name already exists')

      setattr(If, attr_name, cls)

    super(IfMeta, cls).__init__(name, bases, dct)


class If(tuple):
  __metaclass__ = IfMeta

  @classmethod
  def _create(cls, *args):
    return tuple.__new__(cls, args)

  @classmethod
  def _parse(cls, data):
    if isinstance(data, If):
      return data
    else:
      return cls._Value(data)

  def __new__(cls, *args, **kwargs):
    def parse():
      if len(args) <> 0:
        yield cls._And(*args)
      if len(kwargs) <> 0:
        yield cls._Attr(**kwargs)

    return cls._And(*parse())

  def __invert__(self):
    return type(self)._Not(self)

  def __and__(self, other):
    return type(self)._And(self, other)

  def __or__(self, other):
    return type(self)._Or(self, other)

  def __xor__(self, other):
    other = type(self)._parse(other)
    return ((self & ~other) | (~self & other))

  def __add__(self, other):
    return type(self)._Or(self, other)

  def __sub__(self, other):
    other = type(self)._parse(other)
    return (self & ~other)
