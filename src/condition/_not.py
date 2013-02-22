# -*- coding: utf-8 -*-
from operator import itemgetter

from ._is import Is


class Not(Is):
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


@Is._method
def __invert__(self):
  return Not._make(self)
