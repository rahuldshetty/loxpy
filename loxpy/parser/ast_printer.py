from loxpy.parser import expressions
from loxpy.token import Token
from loxpy.token.token_types import TokenType

class AstPrinter(expressions.ExprVisitor):
    def print(self, expr:expressions.Expr):
        return expr.accept(self)

    def parenthesize(self, name, *exprs:expressions.Expr):
        content = ' '.join(expr.accept(self) for expr in exprs)
        return f"({name} {content})"
    
    def visit_binary_expr(self, expr:expressions.Binary):
        return self.parenthesize(
            expr.operator.lexeme,
            expr.left, expr.right
        )
    
    def visit_grouping_expr(self, expr:expressions.Grouping):
        return self.parenthesize("group", expr.expression)
    
    def visit_literal_expr(self, expr:expressions.Literal):
        if expr.value == None:
            return 'null'
        return str(expr.value)

    def visit_unary_expr(self, expr:expressions.Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

if __name__ == "__main__":
    exp = expressions.Binary(
        expressions.Unary(
            Token(TokenType.MINUS, '-', '', 1),
            expressions.Literal(123)
        ),
        Token(TokenType.MULTIPLY, '*', '', 1),
        expressions.Grouping(expressions.Literal(45.67))
    )
    printer = AstPrinter()
    print(printer.print(exp))



