# -*- coding: utf-8 -*-
from ._if import If


class Empty(If):
  def __new__(cls):
    return cls._instance

  def __repr__(self):
    return 'is NOTHING'

Empty._instance = Empty._create()
