# -*- coding: utf-8 -*-
from operator import itemgetter

from ._is import Is


class Value(Is):
  content = property(itemgetter(0))

  def __new__(cls, data):
    return cls._create(data)

  def __repr__(self):
    return '=`%s`' % str(self.content)


@Is._method
@classmethod
def _parse(cls, data):
  if isinstance(data, Is):
    return data
  else:
    return Value._create(data)
