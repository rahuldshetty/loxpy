from loxpy.evaluator.lox_callable import LoxCallable
from loxpy.parser import statements
from loxpy.environment import Environment

from loxpy.evaluator.runtime_error import LoxReturn

from copy import deepcopy

class LoxFunction(LoxCallable):
    def __init__(self, 
        declaration:statements.Function,
        closure:Environment,
        inside_class=False,
        is_initializer=False
    ):
        super().__init__()
        self.declaration = declaration
        self.is_initializer = is_initializer
        if inside_class:
            # Refer to parent closure
            self.closure = closure
        else:
            self.closure = deepcopy(closure)

    def call(self, interpreter, arguments:list):
        env = self.closure

        for i in range(0, len(self.declaration.params), 1):
            arg = self.declaration.params[i]
            env.define(
                arg.lexeme, arguments[i]
            )

        try:
            interpreter.execute_block(self.declaration.body, env)
        except LoxReturn as return_obj:
            if self.is_initializer:
                return self.closure.get("this")

            return return_obj.value 

        if self.is_initializer:
            return self.closure.get("this")
        
        return None

    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"

    def bind(self, instance):
        env = Environment(self.closure)
        env.define("this", instance)
        return LoxFunction(self.declaration, env, True, self.is_initializer)