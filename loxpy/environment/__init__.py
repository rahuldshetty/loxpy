from loxpy.token import Token
from loxpy.evaluator.runtime_error import LoxPyRuntimeError

class Environment:
    def __init__(self):
        self.env_values = {}
    
    def define(self, name, value):
        self.env_values[name] = value
    
    def get(self, name:Token):
        if name.lexeme in self.env_values:
            return self.env_values[name.lexeme]
        raise LoxPyRuntimeError(
            name, "Undefined variable " + name.lexeme + "."
        )
