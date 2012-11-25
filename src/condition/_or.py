# -*- coding: utf-8 -*-
from operator import itemgetter

from ._if import If


class Or(If):
  content = property(itemgetter(0))

  _make = If._And._make
  __new__ = If._And.__new__

  def __repr__(self):
    return '(%s)' % (' || '.join(str(item) for item in self.content))
