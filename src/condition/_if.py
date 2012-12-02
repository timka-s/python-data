# -*- coding: utf-8 -*-
from types import FunctionType


class If(tuple):
  @classmethod
  def _method(cls, fn):
    if type(fn) == FunctionType:
      name = fn.__name__
    else:
      name = fn.__func__.__name__

    setattr(cls, name, fn)

  @classmethod
  def _create(cls, *args):
    return tuple.__new__(cls, args)

  def __new__(cls):
    raise TypeError("This constructor is abstract")
