from expression.expression import Expression, Parameter, Variable
from expression.sign import Sign
import atomic.atom_loader

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
    COMMENT_KEYWORD = '#'

    def __init__(self):
        self.clear()
        self.atom_dict = atomic.atom_loader.generate_atom_dict()

    # Dump previous input.
    def clear(self):
        self.symbol_table = {}
        self.expressions = []

    # Evaluates expression and records the meaning.
    def parse(self, expression):
        toks = expression.split()
        if len(toks) == 0: return

        actions = { 
            Parser.VARIABLE_KEYWORD: self.parse_variables, 
            Parser.PARAMETER_KEYWORD: self.parse_parameters,
            Parser.COMMENT_KEYWORD: lambda *args: None # Do nothing
        }
        
        # If not one of the actions listed, default is to parse expression.
        actions.get(toks[0], self.parse_expression)(toks, expression)   

    # Reads variable names and adds them to the symbol table
    # with an affine Expression as the value.
    def parse_variables(self, tokenized, expression):
        index = 1
        while index < len(tokenized):
            name = tokenized[index]
            self.check_name_conflict(name)
            self.symbol_table[name] = Variable(name)
            index += 1

    # Reads parameter names and adds them to the symbol table
    # with a constant Expression as the value.
    def parse_parameters(self, tokenized, expression):
        if len(tokenized) <= 1: return
        # Check second token for sign
        potential_sign = tokenized[1].upper()
        if Sign.is_sign(potential_sign):
            sign = Sign(potential_sign)
            index = 2
        else:
            sign = Sign.UNKNOWN
            index = 1
        # Read parameters
        while index < len(tokenized):
            name = tokenized[index]
            self.check_name_conflict(name)
            self.symbol_table[name] = Parameter(name, sign)
            index += 1

    # Check if name conflicts with atom name.
    # Variable and parameter names can be overriden.
    def check_name_conflict(self, name):
        if name in self.atom_dict:
            raise Exception('The name %s is reserved for '
                            'an atomic function.' % name)

    # Parses a convex optimization expression (i.e. objective, constraint, or assignment).
    # Adds evaluated expression to expressions list.
    def parse_expression(self, tokenized, expression):
        # TODO constraints
        exp = self.evaluate_expression(expression)
        if isinstance(exp, Expression):
            self.expressions.append(exp)

    # Evaluates an objective (TODO constraint) and returns an
    # Expression that is the root of a full parse tree.
    def evaluate_expression(self, expression):
        # Merge atoms, variables, and parameters.
        local_vars = dict(self.symbol_table.items() + self.atom_dict.items())
        # TODO replace this. Eval is insecure.
        return eval(expression, {"__builtins__": None}, local_vars)