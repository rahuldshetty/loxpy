from loxpy.evaluator.lox_callable import LoxCallable
from loxpy.parser import statements

class LoxFunction(LoxCallable):
    def __init__(self, declaration:statements.Function):
        super().__init__()
        self.declaration = declaration


    def call(self, interpreter, arguments:list):
        env = interpreter.global_env
        for i in range(len(self.declaration.params)):
            arg = self.declaration.params[i]
            env.define(
                arg.lexeme, arguments[i]
            )
        interpreter.execute_block(self.declaration.body, env)

    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
