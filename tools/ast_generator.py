
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, Iterable, Tuple, TextIO

arg_parser = ArgumentParser(usage='generate_ast.py <output directory>')
arg_parser.add_argument('output',
                        help='Directory where the generated result '
                             'will be stored. Default: /lox',
                        )
args = arg_parser.parse_args()

# Constants

INDENTATION = '     '

# Expression Import

DEFAULT_IMPORTS = ('from abc import ABC, abstractmethod',)

EXPRESSION_IMPORTS = DEFAULT_IMPORTS + (
    'from loxpy.scanner import Scanner',
    'from loxpy.token import Token',
)

# Expression CGF production rules

EXPRESSIONS = {
    "Assign": ("name: Token", "value: Expr"),
    "Binary": ('left: Expr', 'operator: Token', 'right: Expr'),
    "Grouping": ('expression: Expr',),
    "Literal": ('value: object',),
    "Logical": ('left: Expr', 'operator: Token', 'right: Expr'),
    "Unary": ('operator: Token', 'right: Expr'),
    "Variable": ("name: Token",),
}

# Statement Import

STATEMENTS_IMPORTS = DEFAULT_IMPORTS + (
    'from loxpy.parser.expressions import Expr',
    'from loxpy.token import Token',
)

STATEMENTS = {
    "Block": ("statements: list",),
    "Break": ("token: Token",),
    "Expression": ("expression: Expr",),
    "If": ( "condition: Expr", "thenBranch: Stmt", "elseBranch: Stmt" ),
    "Print": ("expression: Expr",),
    "Var": ("name: Token", "initializer: Expr"),
    "While": ("condition: Expr", "body: Stmt"),
}


def define_imports(file, lines):
    file.write('\n'.join(lines))

def define_visitor(file, base_name, types):
    name = base_name.lower()
    visitor = f"{base_name}Visitor"

    file.write("\n\n\n")
    file.write(f"class {visitor}(ABC):")

    for typ in types:
        file.write('\n')
        file.write(f'{INDENTATION}@abstractmethod\n')
        file.write(f"{INDENTATION}def visit_{typ.lower()}_{name}(self, expr: '{base_name}'):\n")
        file.write(f"{INDENTATION * 2}pass\n")

def define_type(file, base_name, class_name, fields):
    file.write(f'class {class_name}({base_name}):\n')
    file.write(f'{INDENTATION}def __init__(self, {",".join(fields)}):\n')
    
    for field in fields:
        attr = field.split(":")[0]
        file.write(f"{INDENTATION * 2}self.{attr} = {attr}\n")

    file.write("\n")
    file.write(f"{INDENTATION}def accept(self, visitor: {base_name}Visitor):\n")
    file.write(f"{INDENTATION * 2}return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n")


def define_ast(path:Path, base_name:str, types, imports):
    name = base_name.title()
    visitor = f"{base_name}Visitor"
    
    with path.open(mode='w', encoding='utf-8') as file:
        define_imports(file, imports)
        define_visitor(file, base_name, types.keys())

        file.write('\n\n')
        
        file.write(f'class {name}(ABC):\n')
        file.write(f'{INDENTATION}@abstractmethod\n')
        file.write(f'{INDENTATION}def accept(self, visitor: {visitor}):\n')
        file.write(f"{INDENTATION * 2}pass\n\n")

        for class_name, fields in types.items():
            file.write("\n")
            define_type(file, name, class_name, fields)
            file.write("\n")


def main():
    path = Path(args.output).resolve()

    if not path.is_dir():
        arg_parser.error("Output must be a valid directory")

    define_ast(path / 'expressions.py', 'Expr', EXPRESSIONS, EXPRESSION_IMPORTS)
    define_ast(path / 'statements.py', 'Stmt', STATEMENTS, STATEMENTS_IMPORTS)

if __name__ == "__main__":
    main()