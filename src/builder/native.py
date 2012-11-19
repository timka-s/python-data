# -*- coding: utf-8 -*-
from itertools import chain

from . import byte_code as bc
from .. import condition


class Native(object):
  _lib = {}
  _operation = {}

  @classmethod
  def new_handler(cls, act):
    def handler(fn):
      cls._lib[act] = fn
    return handler

  @classmethod
  def new_operation(cls, act):
    def operation(op):
      if callable(op):
        res = op
      else:
        op = [bc.compare_op(op)]
        res = lambda build, term, level: \
            [bc.load_fast('level_%s' % (level))] + build(term, level) + op
      cls._operation[act] = res
    return operation

  @classmethod
  def build(cls, term, level):
    return cls._lib[type(term)](cls.build, term, level)

  @classmethod
  def make(cls, term):
    code = [
      bc.load_fast('obj'),
      bc.store_fast('level_0'),
    ] + cls.build(term, 0) + [
      bc.return_value(),
    ]

    return bc.compile_code(code, globals())

@Native.new_handler(condition.Empty)
def if_empty(build, term, level):
  return [
    bc.load_const(Native),
  ]

@Native.new_handler(condition.Value)
def if_value(build, term, level):
  return [
    bc.load_const(term.content),
  ]


@Native.new_handler(condition.Field)
def if_field(build, term, level):
  def parse():
    for attr in term.path:
      yield bc.load_attr(attr)
    
  return [
    bc.load_fast('level_%s' % (level - term.depth)),
  ] + list(parse())

@Native.new_handler(condition.Not)
def if_not(build, term, level):
  return build(term.content, level) + [
    bc.unary_not(),
  ]

@Native.new_handler(condition.And)
def if_not(build, terms, level):
  label = bc.label()

  def parse():
    for term in terms.content:
      yield build(term, level) + [
        bc.jump_if_false_or_pop(label),
      ]

  return list(chain.from_iterable(parse())) + [
    bc.load_const(True),
    bc.label(label),
  ]

@Native.new_handler(condition.Or)
def if_not(build, terms, level):
  label = bc.label()

  def parse():
    for term in terms.content:
      yield build(term, level) + [
        bc.jump_if_true_or_pop(label),
      ]

  return list(chain.from_iterable(parse())) + [
    bc.load_const(False),
    bc.label(label),
  ]


@Native.new_handler(condition.Attr)
def if_attr(build, terms, level):
  field = terms.attr
  term = terms.content

  if Native._operation.has_key(field):
    return Native._operation[field](build, term, level)
  else:
    return [
      bc.load_fast('level_%s' % (level)),
      bc.load_attr(field),
      bc.store_fast('level_%s' % (level + 1)),
    ] + build(term, level + 1)


Native.new_operation('EQ')('==')
Native.new_operation('NE')('!=')
Native.new_operation('GT')('>')
Native.new_operation('GE')('>=')
Native.new_operation('LT')('<')
Native.new_operation('LE')('<=')

@Native.new_operation('COUNT')
def op_count(build, term, level):
  return [
    bc.load_const(len),
    bc.load_fast('level_%s' % (level)),
    bc.call_function(1),
    bc.store_fast('level_%s' % (level + 1)),
  ] + build(term, level + 1)

@Native.new_operation('ALL')
def op_all(build, term, level):
  iter_label = bc.label()
  loop_label = bc.label()
  exit_label = bc.label()

  return [
    bc.load_fast('level_%s' % (level)),
    bc.get_iter(),
    bc.label(iter_label),
    bc.for_iter(loop_label),
    bc.store_fast('level_%s' % (level + 1)),
  ] + build(term, level + 1) + [
    bc.pop_jump_if_true(iter_label),
    bc.pop_top(), # Remove the iterator
    bc.load_const(False),
    bc.jump_absolute(exit_label),
    bc.label(loop_label),
    bc.load_const(True),
    bc.label(exit_label),
  ]

@Native.new_operation('ANY')
def op_all(build, term, level):
  iter_label = bc.label()
  loop_label = bc.label()
  exit_label = bc.label()

  return [
    bc.load_fast('level_%s' % (level)),
    bc.get_iter(),
    bc.label(iter_label),
    bc.for_iter(loop_label),
    bc.store_fast('level_%s' % (level + 1)),
  ] + build(term, level + 1) + [
    bc.pop_jump_if_false(iter_label),
    bc.pop_top(), # Remove the iterator
    bc.load_const(True),
    bc.jump_absolute(exit_label),
    bc.label(loop_label),
    bc.load_const(False),
    bc.label(exit_label),
  ]
