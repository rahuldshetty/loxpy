from loxpy.parser import expressions
from loxpy.parser import statements
from loxpy.token import Token
from loxpy.token.token_types import TokenType

from loxpy.environment import Environment

from loxpy.evaluator.runtime_error import LoxPyRuntimeError, LoxPyDivisionByZeroError

class Interpreter(
    expressions.ExprVisitor,
    statements.StmtVisitor
):
    def __init__(self, lox_main):
        self.lox = lox_main
        self.env = Environment()

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except LoxPyRuntimeError as error:
            self.lox.runtime_error(error)

    def execute(self, statement:statements.Stmt):
        statement.accept(self)

    def stringify(self, value):
        if object == None:
            return "null"
        
        if type(value) == float:
            if value.is_integer():
                return str(int(value))
            return str(value)

        if type(value) == bool:
            return 'true' if value else 'false'

        if type(value) == str:
            return '"' + value + '"'

        return str(value)

    def evaluate(self, expr:expressions.Expr):
        return expr.accept(self)

    def is_truthy(self, object:object):
        if object == None:
            return False
        if type(object) == bool:
            return object
        return True
    
    def is_equal(self, left, right):
        if left == None and right == None:
            return True
        if left == None:
            return False
        return left == right
    
    def visit_binary_expr(self, expr:expressions.Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return left - right
        elif expr.operator.type == TokenType.MULTIPLY:
            self.check_number_operands(expr.operator, left, right)
            return left * right
        elif expr.operator.type == TokenType.DIVIDE:
            self.check_number_operands(expr.operator, left, right)
            self.check_divisor_zero(expr.operator, right)
            return left / right
        elif expr.operator.type == TokenType.PLUS:
            if type(left) == type(right) and type(left) == str:
                return left + right
            elif type(left) == type(right) and type(left) == float:
                return left + right
            else:
                raise LoxPyRuntimeError(expr.operator, "Operands must be either number or string type but not both.")
        
        elif expr.operator.type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return left > right
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left >= right
        elif expr.operator.type == TokenType.LESSER:
            self.check_number_operands(expr.operator, left, right)
            return left < right
        elif expr.operator.type == TokenType.LESSER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left <= right
        
        elif expr.operator.type == TokenType.NOT_EQUAL:
            return not self.is_equal(left, right)
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)
        
        return None

    
    def visit_grouping_expr(self, expr:expressions.Grouping):
        return self.evaluate(expr.expression)
    
    def visit_literal_expr(self, expr:expressions.Literal):
        return expr.value
    
    def visit_unary_expr(self, expr:expressions.Unary):
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.NOT:
            return not self.is_truthy(right)
        if expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)
        
        return None
    
    def visit_expression_stmt(self, expr: statements.Expression):
        self.evaluate(expr.expression)
        return None
    
    def visit_print_stmt(self, expr: statements.Print):
        value = self.evaluate(expr.expression)
        print(self.stringify(value))
        return None

    def visit_var_stmt(self, stmt: statements.Var):
        value = None
        if stmt.initializer != None:
            value = self.evaluate(stmt.initializer)
        self.env.define(stmt.name.lexeme, value)
    
    def visit_variable_expr(self, expr: expressions.Variable):
        return self.env.get(expr.name)

    def visit_assign_expr(self, expr: expressions.Assign):
        value = self.evaluate(expr.value)
        self.env.assign(expr.name, value)
        return value

    def check_number_operand(self, operator:Token, operand:object):
        if type(operand) == float:
            return
        raise LoxPyRuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator:Token, left:object, right:object):
        if type(left) == float and type(right) == float:
            return
        raise LoxPyRuntimeError(operator, "Operand must be a numbers.")
    
    def check_divisor_zero(self, operator:Token, divisor:float):
        if divisor == 0:
            raise LoxPyDivisionByZeroError(operator)


