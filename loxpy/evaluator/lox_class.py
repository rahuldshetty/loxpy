from loxpy.evaluator.lox_instance import LoxInstance
from loxpy.evaluator.lox_callable import LoxCallable


class LoxClass(LoxCallable):

    def __init__(self, name, methods:list):
        self.name = name
        self.methods = methods
    
    def __str__(self):
        return self.name

    def call(self, interpreter, arguments: list):
        lox_instance = LoxInstance(self)
        return lox_instance

    def arity(self):
        return 0
    
    def find_method(self, name):
        if name in self.methods:
            return self.methods[name]
