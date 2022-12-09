
class LoxPyRuntimeError(RuntimeError):
    def __init__(self, token, message):
        self.token = token
        super().__init__(message)
        
class LoxPyDivisionByZeroError(LoxPyRuntimeError):
    def __init__(self, token):
        super().__init__(token, "You cannot divide number by 0.")