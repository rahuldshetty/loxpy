from loxpy.token import Token
from loxpy.evaluator.runtime_error import LoxPyRuntimeError

class Environment:
    def __init__(self, enclosing=None):
        self.env_values = {}
        self.enclosing:Environment = enclosing
    
    def define(self, name:str, value:object):
        self.env_values[name] = value

    def get(self, name:Token):
        if name.lexeme in self.env_values:
            return self.env_values[name.lexeme]

        if self.enclosing != None:
            return self.enclosing.get(name)

        raise LoxPyRuntimeError(
            name, "Undefined variable " + name.lexeme + "."
        )

    def assign(self, name:Token, value:object):
        if name.lexeme in self.env_values:
            self.env_values[name.lexeme] = value
            return

        if self.enclosing != None:
            self.enclosing.assign(name, value)
            return

        raise LoxPyRuntimeError(
            name, "Undefined variable " + name.lexeme + "."
        )
