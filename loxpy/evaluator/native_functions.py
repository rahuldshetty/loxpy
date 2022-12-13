import time
from loxpy.evaluator.lox_callable import LoxCallable

class Clock(LoxCallable):

    def call(self, interpreter, arguments):
        return float(time.perf_counter())

    def arity(self):
        return 0

    def __str__(self):
        return "<Native function 'clocl'>"
