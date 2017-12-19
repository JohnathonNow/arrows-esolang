#!/usr/bin/env python
from enum import Enum
from arrows_esolang.Action import *

__statement_label__ = 0

class NodeType(Enum):
    ACTION = 0
    CONDITIONAL = 1

class Statement(object):
    def __init__(self):
        global __statement_label__
        self.kind = None
        self.if_zero = None
        self.if_else = None
        self.next = None
        self.actions = []
        self.label = __statement_label__
        __statement_label__ += 1

    def add_add(self, register):
        if register > 0:
            self.actions.append(Action(ActionType.ADD, register))

    def add_action(self, kind, register):
        self.add_add(register)
        self.actions.append(Action(kind))
