# -*- coding: utf-8 -*-
from types import FunctionType

from byteplay import (
  Code, Label, POP_TOP, LOAD_FAST, STORE_FAST, LOAD_CONST, LOAD_ATTR,
  GET_ITER, FOR_ITER, UNARY_NOT, COMPARE_OP, CALL_FUNCTION,
  JUMP_IF_TRUE_OR_POP, JUMP_IF_FALSE_OR_POP, JUMP_ABSOLUTE,
  POP_JUMP_IF_TRUE, POP_JUMP_IF_FALSE, RETURN_VALUE)


def compile_code(code, gobj = globals()):
  return FunctionType(
      Code(
          code, tuple(), ('obj',), False, False, True,
          "<code>", "<auto_generated>", 0, "auto generated code"
      ).to_code(),
      gobj
  )

def label(label = None):
  if label is None:
    return Label()
  else:
    return (label, None)

def pop_top():
  return (POP_TOP, None)

def load_fast(vname):
  return (LOAD_FAST, vname)

def store_fast(vname):
  return (STORE_FAST, vname)

def load_const(val):
  return (LOAD_CONST, val)

def load_attr(attr):
  return (LOAD_ATTR, attr)

def get_iter():
  return (GET_ITER, None)

def for_iter(label):
  return (FOR_ITER, label)

def unary_not():
  return (UNARY_NOT, None)

def compare_op(op):
  return (COMPARE_OP, op)

def call_function(arg_count):
  return (CALL_FUNCTION, arg_count)

def jump_if_true_or_pop(label):
  return (JUMP_IF_TRUE_OR_POP, label)

def jump_if_false_or_pop(label):
  return (JUMP_IF_FALSE_OR_POP, label)

def jump_absolute(label):
  return (JUMP_ABSOLUTE, label)

def pop_jump_if_true(label):
  return (POP_JUMP_IF_TRUE, label)

def pop_jump_if_false(label):
  return (POP_JUMP_IF_FALSE, label)

def return_value():
  return (RETURN_VALUE, None)
