from expression.expression import *
from expression.sign import Sign

class Parser(object):
    """
    Parses convex optimization problems.
    Permitted expressions:
      variable x y z ...
      parameter (SIGN) a b c ...
      Any constraint or objective.
    """
    # Keywords
    VARIABLE_KEYWORD = 'variable'
    PARAMETER_KEYWORD = 'parameter'

    def __init__(self):
        self.clear()

    # Dump previous input.
    def clear(self):
        self.symbol_table = {}
        self.expressions = []

    def parse(self, expression):
        tokenized = expression.split()
        if len(tokenized) == 0:
            return None
        elif tokenized[0] == 'variable':
            self.parse_variables(tokenized)
        elif tokenized[0] == 'parameter':
            self.parse_parameters(tokenized)
        else:
            self.expressions.append(self.evaluate_expression(expression))


    # Reads variable names and adds them to the symbol table
    # with an affine Expression as the value.
    def parse_variables(self, tokenized):
        index = 1
        while index < len(tokenized):
            name = tokenized[index]
            self.symbol_table[name] = Variable(name)
            index += 1

    # Reads parameter names and adds them to the symbol table
    # with a constant Expression as the value.
    def parse_parameters(self, tokenized):
        if len(tokenized) <= 1: return
        # Check second token for sign
        potential_sign = tokenized[1].upper()
        if Sign.is_sign(potential_sign):
            sign = Sign(potential_sign)
            index = 2
        else:
            sign = Sign(Sign.UNKNOWN_KEY)
            index = 1
        # Read parameters
        while index < len(tokenized):
            name = tokenized[index]
            self.symbol_table[name] = Parameter(name, sign)
            index += 1

    # Evaluates a constraint or objective and returns an
    # Expression TODO with the full parse tree.
    def evaluate_expression(self, expression):
        # Restrict global namespace in eval for security.
        return eval(expression, {"__builtins__":None}, self.symbol_table)
