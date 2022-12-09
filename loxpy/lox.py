from . import __VERSION__

import sys

from loxpy.scanner import Scanner
from loxpy.parser import Parser
from loxpy.evaluator import Interpreter
from loxpy.evaluator.runtime_error import LoxPyRuntimeError
from loxpy.parser.ast_printer import AstPrinter

class Lox:
    hasError = False
    hasRuntimeError = False

    def __init__(self):
        pass
    
    @staticmethod
    def error(line, message):
        Lox.report(line, "", message)

    @staticmethod
    def runtime_error(error:LoxPyRuntimeError):
        Lox.report(error.token.line, "", str(error))

    @staticmethod
    def report(line, where, message):
        sys.stderr.write(f"[line {line}] Error {where}: {message}\n")
        sys.stderr.flush()
        Lox.hasError = True

    def run(self, source):
        scanner = Scanner(source, self)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens, self)
        expression = parser.parse()

        interpreter = Interpreter(self)

        if self.hasError:
            return
        
        interpreter.interpret(expression)

        # print(AstPrinter().print(expression))
    
    def run_file(self, script):
        try:
            fh = open(script, 'r')
            script_data = fh.read()
            fh.close()
            self.run(script_data)
            if Lox.hasError:
                sys.exit(65)
            if Lox.hasRuntimeError:
                sys.exit(70)
        except FileNotFoundError:
            sys.exit(1)
        
    def run_prompt(self):
        platform = sys.platform
        sys.stdout.write(f"loxPy Interpreter {__VERSION__} ({platform})\n")
        sys.stdout.flush()
        while True:
            try:
                line = input('> ')
                self.run(line)
                Lox.hasError = False
            except EOFError:
                break   


    def error_code(self):
        pass