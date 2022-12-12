
class LoxBreakException(RuntimeError):
    def __init__(self, token):
        self.token = token
        super().__init__(f"Break statement found at line {self.token.line}.")

class LoxPyRuntimeError(RuntimeError):
    def __init__(self, token, message):
        self.token = token
        super().__init__(message)
        
class LoxPyDivisionByZeroError(LoxPyRuntimeError):
    def __init__(self, token):
        super().__init__(token, "You cannot divide number by 0.")