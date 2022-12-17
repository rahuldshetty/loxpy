from abc import ABC, abstractmethod
from loxpy.parser.expressions import Expr, Variable
from loxpy.token import Token


class StmtVisitor(ABC):
     @abstractmethod
     def visit_block_stmt(self, expr: 'Stmt'):
          pass

     @abstractmethod
     def visit_class_stmt(self, expr: 'Stmt'):
          pass

     @abstractmethod
     def visit_break_stmt(self, expr: 'Stmt'):
          pass

     @abstractmethod
     def visit_expression_stmt(self, expr: 'Stmt'):
          pass

     @abstractmethod
     def visit_function_stmt(self, expr: 'Stmt'):
          pass

     @abstractmethod
     def visit_if_stmt(self, expr: 'Stmt'):
          pass

     @abstractmethod
     def visit_print_stmt(self, expr: 'Stmt'):
          pass

     @abstractmethod
     def visit_return_stmt(self, expr: 'Stmt'):
          pass

     @abstractmethod
     def visit_var_stmt(self, expr: 'Stmt'):
          pass

     @abstractmethod
     def visit_while_stmt(self, expr: 'Stmt'):
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


class Class(Stmt):
     def __init__(self, name: Token,superclass: Variable,methods: list):
          self.name = name
          self.superclass = superclass
          self.methods = methods

     def accept(self, visitor: StmtVisitor):
          return visitor.visit_class_stmt(self)


class Break(Stmt):
     def __init__(self, token: Token):
          self.token = token

     def accept(self, visitor: StmtVisitor):
          return visitor.visit_break_stmt(self)


class Expression(Stmt):
     def __init__(self, expression: Expr):
          self.expression = expression

     def accept(self, visitor: StmtVisitor):
          return visitor.visit_expression_stmt(self)


class Function(Stmt):
     def __init__(self, name: Token,params: list,body: list):
          self.name = name
          self.params = params
          self.body = body

     def accept(self, visitor: StmtVisitor):
          return visitor.visit_function_stmt(self)


class If(Stmt):
     def __init__(self, condition: Expr,thenBranch: Stmt,elseBranch: Stmt):
          self.condition = condition
          self.thenBranch = thenBranch
          self.elseBranch = elseBranch

     def accept(self, visitor: StmtVisitor):
          return visitor.visit_if_stmt(self)


class Print(Stmt):
     def __init__(self, expression: Expr):
          self.expression = expression

     def accept(self, visitor: StmtVisitor):
          return visitor.visit_print_stmt(self)


class Return(Stmt):
     def __init__(self, keyword: Token,value: Expr):
          self.keyword = keyword
          self.value = value

     def accept(self, visitor: StmtVisitor):
          return visitor.visit_return_stmt(self)


class Var(Stmt):
     def __init__(self, name: Token,initializer: Expr):
          self.name = name
          self.initializer = initializer

     def accept(self, visitor: StmtVisitor):
          return visitor.visit_var_stmt(self)


class While(Stmt):
     def __init__(self, condition: Expr,body: Stmt):
          self.condition = condition
          self.body = body

     def accept(self, visitor: StmtVisitor):
          return visitor.visit_while_stmt(self)

