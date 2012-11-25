# -*- coding: utf-8 -*-


class SimpleNamespace:
  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)

  def __repr__(self):
    keys = reversed(self.__dict__.keys())
    items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
    return "{}({})".format(type(self).__name__, ", ".join(items))
