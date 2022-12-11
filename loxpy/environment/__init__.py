from loxpy.token import Token
from loxpy.evaluator.runtime_error import LoxPyRuntimeError

class Environment:
    def __init__(self):
        self.env_values = {}
    
    def define(self, name:str, value:object):
        self.env_values[name] = value

    def get(self, name:Token):
        if name.lexeme in self.env_values:
            return self.env_values[name.lexeme]
        raise LoxPyRuntimeError(
            name, "Undefined variable " + name.lexeme + "."
        )

    def assign(self, name:Token, value:object):
        if name.lexeme in self.env_values:
            self.env_values[name.lexeme] = value
            return
        raise LoxPyRuntimeError(
            name, "Undefined variable " + name.lexeme + "."
        )
