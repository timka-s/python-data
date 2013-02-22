# -*- coding: utf-8 -*-
from operator import itemgetter

from ._is import Is


class Field(Is):
  source = property(itemgetter(0))
  depth = property(itemgetter(1))
  path = property(itemgetter(2))

  def __new__(cls, src):
    outer = src.lstrip('.')
    return cls._create(src, len(src) - len(outer), outer.split('__'))

  def __repr__(self):
    return '=%s' % str(self.source)
