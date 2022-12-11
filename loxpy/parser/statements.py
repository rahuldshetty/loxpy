from abc import ABC, abstractmethod
from loxpy.parser.expressions import Expr
from loxpy.token import Token


class StmtVisitor(ABC):
     @abstractmethod
     def visit_block_stmt(self, expr: 'Stmt'):
          pass

     @abstractmethod
     def visit_expression_stmt(self, expr: 'Stmt'):
          pass

     @abstractmethod
     def visit_print_stmt(self, expr: 'Stmt'):
          pass

     @abstractmethod
     def visit_var_stmt(self, expr: 'Stmt'):
          pass


class Stmt(ABC):
     @abstractmethod
     def accept(self, visitor: StmtVisitor):
          pass


class Block(Stmt):
     def __init__(self, statements: list):
          self.statements = statements

     def accept(self, visitor: StmtVisitor):
          return visitor.visit_block_stmt(self)


class Expression(Stmt):
     def __init__(self, expression: Expr):
          self.expression = expression

     def accept(self, visitor: StmtVisitor):
          return visitor.visit_expression_stmt(self)


class Print(Stmt):
     def __init__(self, expression: Expr):
          self.expression = expression

     def accept(self, visitor: StmtVisitor):
          return visitor.visit_print_stmt(self)


class Var(Stmt):
     def __init__(self, name: Token,initializer: Expr):
          self.name = name
          self.initializer = initializer

     def accept(self, visitor: StmtVisitor):
          return visitor.visit_var_stmt(self)

