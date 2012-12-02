# -*- coding: utf-8 -*-
from operator import itemgetter

from ._if import If


class Not(If):
  content = property(itemgetter(0))

  @classmethod
  def _make(cls, data):
    if isinstance(data, cls):
      return data.content
    else:
      return cls._create(data)

  def __new__(cls, data):
    return cls._make(cls._parse(data))

  def __repr__(self):
    return '~%s' % str(self.content)


@If._method
def __invert__(self):
  return Not._make(self)
