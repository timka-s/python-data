# -*- coding: utf-8 -*-
from types import FunctionType

from byteplay import (
  Code, Label, POP_TOP, LOAD_FAST, STORE_FAST, LOAD_CONST, LOAD_ATTR,
  GET_ITER, FOR_ITER, UNARY_NOT, COMPARE_OP, CALL_FUNCTION,
  JUMP_IF_TRUE_OR_POP, JUMP_IF_FALSE_OR_POP, JUMP_ABSOLUTE,
  POP_JUMP_IF_TRUE, POP_JUMP_IF_FALSE, RETURN_VALUE)


def compileCode(code, gobj = globals()):
  return FunctionType(
      Code(
          code, tuple(), ('obj',), False, False, True,
          "<code>", "<auto_generated>", 0, "auto generated code"
      ).to_code(),
      gobj
  )

def makeLabel():
  return Label()

def putLabel(label):
  return (label, None)

def popTop():
  return (POP_TOP, None)

def loadFast(vname):
  return (LOAD_FAST, vname)

def storeFast(vname):
  return (STORE_FAST, vname)

def loadConst(val):
  return (LOAD_CONST, val)

def loadAttr(attr):
  return (LOAD_ATTR, attr)

def getIter():
  return (GET_ITER, None)

def forIter(label):
  return (FOR_ITER, label)

def unaryNot():
  return (UNARY_NOT, None)

def compareOp(op):
  return (COMPARE_OP, op)

def callFunction(arg_count):
  return (CALL_FUNCTION, arg_count)

def jumpIfTrueOrPop(label):
  return (JUMP_IF_TRUE_OR_POP, label)

def jumpIfFalseOrPop(label):
  return (JUMP_IF_FALSE_OR_POP, label)

def jumpAbsolute(label):
  return (JUMP_ABSOLUTE, label)

def popJumpIfTrue(label):
  return (POP_JUMP_IF_TRUE, label)

def popJumpIfFalse(label):
  return (POP_JUMP_IF_FALSE, label)

def returnValue():
  return (RETURN_VALUE, None)
