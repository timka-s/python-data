# -*- coding: utf-8 -*-
from operator import itemgetter

from ._is import Is
from ._and import And


class Or(Is):
  content = property(itemgetter(0))

  _make = And._make
  __new__ = And.__new__

  def __repr__(self):
    return '(%s)' % (' || '.join(str(item) for item in self.content))


@Is._method
def __or__(self, other):
  return Or(self, other)

@Is._method
def __add__(self, other):
  return Or(self, other)
