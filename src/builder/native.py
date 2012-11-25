# -*- coding: utf-8 -*-
from itertools import chain

from . import byte_code as bc
from .. import condition


def loadLevel(level):
  return bc.loadFast('level_%s' % level)

def storeLevel(level):
  return bc.storeFast('level_%s' % level)


class Native(object):
  _lib = {}
  _operation = {}

  @classmethod
  def _newType(cls, act):
    def _type(fn):
      cls._lib[act] = fn
    return _type

  @classmethod
  def _newOperation(cls, act):
    def operation(op):
      if callable(op):
        res = op
      else:
        op = [bc.compareOp(op)]
        res = lambda build, term, level: \
            [loadLevel(level)] + build(term, level) + op
      cls._operation[act] = res
    return operation

  @classmethod
  def build(cls, term, level):
    return cls._lib[type(term)](cls.build, term, level)

  @classmethod
  def make(cls, term):
    code = [
      bc.loadFast('obj'),
      storeLevel(0),
    ] + cls.build(term, 0) + [
      bc.returnValue(),
    ]

    return bc.compileCode(code, globals())

@Native._newType(condition.Empty)
def if_empty(build, term, level):
  return [
    bc.loadConst(Native),
  ]

@Native._newType(condition.Value)
def if_value(build, term, level):
  return [
    bc.loadConst(term.content),
  ]


@Native._newType(condition.Field)
def if_field(build, term, level):
  def parse():
    for attr in term.path:
      yield bc.loadAttr(attr)
    
  return [
    loadLevel(level - term.depth),
  ] + list(parse())

@Native._newType(condition.Not)
def if_not(build, term, level):
  return build(term.content, level) + [
    bc.unaryNot(),
  ]

@Native._newType(condition.And)
def if_not(build, terms, level):
  label = bc.makeLabel()

  def parse():
    for term in terms.content:
      yield build(term, level) + [
        bc.jumpIfFalseOrPop(label),
      ]

  return list(chain.from_iterable(parse())) + [
    bc.loadConst(True),
    bc.putLabel(label),
  ]

@Native._newType(condition.Or)
def if_not(build, terms, level):
  label = bc.makeLabel()

  def parse():
    for term in terms.content:
      yield build(term, level) + [
        bc.jumpIfTrueOrPop(label),
      ]

  return list(chain.from_iterable(parse())) + [
    bc.loadConst(False),
    bc.putLabel(label),
  ]


@Native._newType(condition.Attr)
def if_attr(build, terms, level):
  field = terms.attr
  term = terms.content

  if Native._operation.has_key(field):
    return Native._operation[field](build, term, level)
  else:
    return [
      loadLevel(level),
      bc.loadAttr(field),
      storeLevel(level + 1),
    ] + build(term, level + 1)


Native._newOperation('EQ')('==')
Native._newOperation('NE')('!=')
Native._newOperation('GT')('>')
Native._newOperation('GE')('>=')
Native._newOperation('LT')('<')
Native._newOperation('LE')('<=')
Native._newOperation('IN')('in')

@Native._newOperation('COUNT')
def op_count(build, term, level):
  return [
    bc.loadConst(len),
    loadLevel(level),
    bc.callFunction(1),
    storeLevel(level + 1),
  ] + build(term, level + 1)

@Native._newOperation('ALL')
def op_all(build, term, level):
  iter_label = bc.makeLabel()
  loop_label = bc.makeLabel()
  exit_label = bc.makeLabel()

  return [
    loadLevel(level),
    bc.getIter(),
    bc.putLabel(iter_label),
    bc.forIter(loop_label),
    storeLevel(level + 1),
  ] + build(term, level + 1) + [
    bc.popJumpIfTrue(iter_label),
    bc.popTop(), # Remove the iterator
    bc.loadConst(False),
    bc.jumpAbsolute(exit_label),
    bc.putLabel(loop_label),
    bc.loadConst(True),
    bc.putLabel(exit_label),
  ]

@Native._newOperation('ANY')
def op_all(build, term, level):
  iter_label = bc.makeLabel()
  loop_label = bc.makeLabel()
  exit_label = bc.makeLabel()

  return [
    loadLevel(level),
    bc.getIter(),
    bc.putLabel(iter_label),
    bc.forIter(loop_label),
    storeLevel(level + 1),
  ] + build(term, level + 1) + [
    bc.popJumpIfFalse(iter_label),
    bc.popTop(), # Remove the iterator
    bc.loadConst(True),
    bc.jumpAbsolute(exit_label),
    bc.putLabel(loop_label),
    bc.loadConst(False),
    bc.putLabel(exit_label),
  ]
