# -*- coding: utf-8 -*-


class If(tuple):
  @staticmethod
  def _type(name):
    def reg(cls):
      setattr(If, '_type_' + name, cls)
      return cls

    return reg

  @classmethod
  def _new(cls, *args):
    return tuple.__new__(cls, args)

  @classmethod
  def _parse(cls, data):
    if isinstance(data, If):
      return data
    elif isinstance(data, dict):
      return cls._type_attr(**data)
    elif isinstance(data, (tuple, list, set)):
      return cls._type_or(*data)
    else:
      return cls._type_value(data)

  def __new__(cls, *args, **kwargs):
    def parse():
      if len(args) <> 0:
        yield args
      if len(kwargs) <> 0:
        yield kwargs

    return cls._type_and(*parse())

  def __invert__(self):
    return type(self)._type_not(self)

  def __and__(self, other):
    return type(self)._type_and(self, other)

  def __or__(self, other):
    return type(self)._type_or(self, other)

  def __xor__(self, other):
    other = type(self)._parse(other)
    return ((self & ~other) | (~self & other))

  def __add__(self, other):
    return type(self)._type_or(self, other)

  def __sub__(self, other):
    other = type(self)._parse(other)
    return (self & ~other)
