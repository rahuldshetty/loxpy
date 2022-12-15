'''
Runtime representation of an instance
'''
from loxpy.token import Token

from loxpy.evaluator.runtime_error import LoxPyRuntimeError

class LoxInstance:
    
    def __init__(self, klass):
        self.kclass = klass
        self.fields = {}

    def __str__(self):
        return self.kclass.name + " instance"

    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        raise LoxPyRuntimeError(name, "Undefined property '" + name.lexeme + "'.")
    
    def set(self, name: Token, value:object):
        self.fields[name.lexeme] = value
