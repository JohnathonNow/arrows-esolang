#!/usr/bin/env python
from enum import Enum

class ActionType(Enum):
    END = 0
    ADD = 1
    PUSH_LEFT = 2
    SUBTRACT_LEFT = 3
    PUSH_RIGHT = 4
    SUBTRACT_RIGHT = 5
    PRINT = 6
    READ = 7

class Action(object):
    def __init__(self, kind, value=None):
        self.kind = kind
        self.value = value

