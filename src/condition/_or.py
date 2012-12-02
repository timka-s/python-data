# -*- coding: utf-8 -*-
from operator import itemgetter

from ._if import If
from ._and import And


class Or(If):
  content = property(itemgetter(0))

  _make = And._make
  __new__ = And.__new__

  def __repr__(self):
    return '(%s)' % (' || '.join(str(item) for item in self.content))


@If._method
def __or__(self, other):
  return Or(self, other)

@If._method
def __add__(self, other):
  return Or(self, other)
