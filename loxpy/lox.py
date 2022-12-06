import sys

from loxpy.scanner import Scanner
from . import __VERSION__

class Lox:
    def __init__(self):
        self.hasError = False

    def error(self, line, message):
        self.report(line, "", message)

    def report(self, line, where, message):
        sys.stderr.write(f"[line {line}] Error {where} : {message}")
        sys.stderr.flush()
        self.hasError = True

    def run(self, source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            sys.stdout.write(token)
            sys.stdout.flush()
    
    def run_file(self, script):
        try:
            fh = open(script, 'r')
            script_data = fh.read()
            fh.close()
            self.run(script_data)
            if self.hasError:
                sys.exit(65)
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
                self.hasError = False
            except EOFError:
                break   


    def error_code(self):
        pass