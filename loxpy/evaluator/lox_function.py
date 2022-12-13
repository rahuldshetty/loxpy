from loxpy.evaluator.lox_callable import LoxCallable
from loxpy.parser import statements

from loxpy.evaluator.runtime_error import LoxReturn

from copy import deepcopy

class LoxFunction(LoxCallable):
    def __init__(self, declaration:statements.Function):
        super().__init__()
        self.declaration = declaration

    def call(self, interpreter, arguments:list):
        env = deepcopy(interpreter.global_env)
        for i in range(0, len(self.declaration.params), 1):
            arg = self.declaration.params[i]
            env.define(
                arg.lexeme, arguments[i]
            )

        try:
            interpreter.execute_block(self.declaration.body, env)
        except LoxReturn as return_obj:
            return return_obj.value
        
        return None

    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
