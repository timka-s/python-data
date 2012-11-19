# -*- coding: utf-8 -*-
from operator import itemgetter

from ._if import If


@If._type('value')
class Value(If):
  content = property(itemgetter(0))

  def __new__(cls, data):
    return cls._new(data)

  def __repr__(self):
    return '=`%s`' % str(self.content)
