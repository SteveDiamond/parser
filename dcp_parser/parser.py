from expression.statement import Statement
from expression.expression import Parameter, Variable
from expression.sign import Sign
import atomic.atom_loader

class Parser(object):
    """
    Parses convex optimization problems.
    Permitted statements:
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
        self.statements = []

    # Evaluates statement and records the meaning.
    def parse(self, statement):
        toks = statement.split()
        if len(toks) == 0: return

        actions = { 
            Parser.VARIABLE_KEYWORD: 
                lambda tokenized, statement: self.parse_inputs(tokenized, statement, Variable),
            Parser.PARAMETER_KEYWORD:
                lambda tokenized, statement: self.parse_inputs(tokenized, statement, Parameter),
            Parser.COMMENT_KEYWORD: lambda *args: None # Do nothing
        }
        
        # If not one of the actions listed, default is to parse statement.
        actions.get(toks[0], self.parse_statement)(toks, statement)   

    # Reads variable or parameter names and adds them to the symbol table.
    # Sign may be specified.
    def parse_inputs(self, tokenized, statement, clazz):
        if len(tokenized) <= 1: return
        # Check second token for sign
        potential_sign = tokenized[1].upper()
        if Sign.is_sign(potential_sign):
            sign = Sign(potential_sign)
            index = 2
        else:
            sign = Sign.UNKNOWN
            index = 1
        # Read variables/parameters
        while index < len(tokenized):
            name = tokenized[index]
            self.check_name_conflict(name)
            self.symbol_table[name] = clazz(name, sign)
            index += 1

    # Check if name conflicts with atom name.
    # Variable and parameter names can be overriden.
    def check_name_conflict(self, name):
        if name in self.atom_dict:
            raise Exception('The name %s is reserved for '
                            'an atomic function.' % name)

    # Parses a convex optimization statement (i.e. objective or constraint).
    # Adds evaluated statements to statements list.
    def parse_statement(self, tokenized, statement):
        exp = self.evaluate_statement(statement)
        if isinstance(exp, Statement):
            self.statements.append(exp)

    # Evaluates an objective or constraint and returns an
    # Statement that is the root of a full parse tree.
    def evaluate_statement(self, statement):
        # Merge atoms, variables, and parameters.
        local_vars = dict(self.symbol_table.items() + self.atom_dict.items())
        # TODO replace this. Eval is insecure.
        return eval(statement, {"__builtins__": None}, local_vars)