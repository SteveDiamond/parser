from expression.statement import Statement
from expression.expression import Parameter, Variable, Constant
from expression.sign import Sign
import atomic.atom_loader
import ply.yacc

class Parser(object):
    """
    Parses convex optimization problems.
    Permitted statements:
      variable (SIGN) x y z ...
      parameter (SIGN) a b c ...
      Any constraint or objective.
    """
    def __init__(self):
        self.clear()
        self.atom_dict = atomic.atom_loader.generate_atom_dict()
        self.parser = self.build_parser()

    # Dump previous input.
    def clear(self):
        self.symbol_table = {}
        self.statements = []

    # Evaluates statement and records the meaning.
    def parse(self, statement):
        self.parser.parse(statement)

    """
    Constructs at lex/yacc parser for convex optimization expressions.
    Based on http://www.dabeaz.com/ply/example.html
    """
    def build_parser(self):
        # Lexer definition

        # Reserved keywords
        reserved = {
           'variable' : 'VARIABLE',
           'parameter' : 'PARAMETER',
            str(Sign.POSITIVE).lower() : 'SIGN',
            str(Sign.NEGATIVE).lower() : 'SIGN',
            str(Sign.ZERO).lower() : 'SIGN',
            str(Sign.UNKNOWN).lower() : 'SIGN',
            'Inf' : 'STRING_ARG', # Special string arguments for atomic functions.
        }

        tokens = [
            'INT','FLOAT',
            'PLUS','MINUS','TIMES','DIVIDE',
            'EQUALS','GEQ','LEQ',
            'LPAREN','RPAREN','COMMA',
            'ID'] + list(set(reserved.values()))

        # Tokens
        t_PLUS    = r'\+'
        t_MINUS   = r'-'
        t_TIMES   = r'\*'
        t_DIVIDE  = r'/'
        t_EQUALS  = r'=='
        t_LEQ     = r'<='
        t_GEQ     = r'>='
        t_LPAREN  = r'\('
        t_RPAREN  = r'\)'
        t_COMMA   = r','

        # Convert IDs to reserved words.
        def t_ID(t):
            r'[a-zA-Z_][a-zA-Z_0-9]*'
            t.type = reserved.get(t.value,'ID') # Check for reserved words
            return t

        # Convert float string to value.
        def t_FLOAT(t):
            r'\d*\.\d+'
            t.value = float(t.value)
            return t

        # Convert integer string to value.
        def t_INT(t):
            r'\d+'
            t.value = int(t.value) 
            return t

        # Ignore whitespace and comments.
        t_ignore_COMMENT = r'\#.*'
        t_ignore = " \t"

        def t_newline(t):
            r'\n+'
            t.lexer.lineno += t.value.count("\n")
            
        def t_error(t):
            if t.value[0] == '=':
                raise Exception("'=' is not valid. Did you mean '=='?")
            elif t.value[0] == '^':
                raise Exception("'^' is not valid. Consider using the 'pow' function.")
            else:
                raise Exception("Illegal character '%s'." % t.value[0])
            
        # Build the lexer
        import ply.lex as lex
        lex.lex()

        # Parser definition
        precedence = (
            ('nonassoc', 'EQUALS', 'LEQ', 'GEQ'),
            ('left','PLUS','MINUS'),
            ('left','TIMES','DIVIDE'),
            ('right','UMINUS', 'UPLUS'),
            )

        # Handle empty input
        def p_statement_empty(t):
            'statement : '

        # Add variables to the symbol table.
        # Variable sign is optional.
        def p_statement_variables(t):
            '''statement : VARIABLE SIGN id_list
                         | VARIABLE id_list
            '''
            sign = Sign.UNKNOWN
            if len(t) == 4: # With sign
                sign = Sign(t[2])
            variables = t[len(t)-1]
            # Add the variables to the symbol table
            for id in variables:
                self.symbol_table[id] = Variable(id, sign)

        # Add parameters to the symbol table.
        # Parameter sign is optional.
        def p_statement_parameters(t):
            '''statement : PARAMETER SIGN id_list
                         | PARAMETER id_list
            '''
            sign = Sign.UNKNOWN
            if len(t) == 4: # With sign
                sign = Sign(t[2])
            parameters = t[len(t)-1]
            # Add the parameters to the symbol table
            for id in parameters:
                self.symbol_table[id] = Parameter(id, sign)

        # List of ids.
        def p_id_list(t):
            '''id_list : ID
                       | id_list ID '''
            if len(t) == 2: # Single id.
                t[0] = [t[1]]
            else: # Concatenated ids.
                t[1].append(t[2])
                t[0] = t[1]

        # Evaluate an expression.
        def p_statement_expr(t):
            '''statement : expression'''
            self.statements.append(t[1])

        # Binary arithmetic and boolean operators.
        def p_expression_binop(t):
            '''expression : expression PLUS expression
                          | expression MINUS expression
                          | expression TIMES expression
                          | expression DIVIDE expression
                          | expression EQUALS expression
                          | expression LEQ expression
                          | expression GEQ expression'''
            if t[2] == '+'  : t[0] = t[1] + t[3]
            elif t[2] == '-': t[0] = t[1] - t[3]
            elif t[2] == '*': t[0] = t[1] * t[3]
            elif t[2] == '/': t[0] = t[1] / t[3]
            elif t[2] == '==': t[0] = t[1].__eq__(t[3])
            elif t[2] == '<=': t[0] = t[1].__le__(t[3])
            elif t[2] == '>=': t[0] = t[1].__ge__(t[3])

        # Error production for arithmetic operators missing arguments.
        def p_expression_binop_error(t):
            '''expression : PLUS
                          | MINUS
                          | TIMES
                          | DIVIDE
                          | EQUALS
                          | LEQ
                          | GEQ'''
            raise Exception("Unexpected '%s'." % t[1])

        # Utility function to convert an atom and expression list to a string.
        # Returns the function call as a string and whether there are missing
        # arguments.
        def get_atom_string(atom, expression_list):
            args = [str(arg) for arg in expression_list]
            missing_args = '' in args
            return (atom + "(" + ", ".join(args) + ")", missing_args)

        # Atomic function.
        def p_expression_atom(t):
            'expression : ID LPAREN expression_list RPAREN'
            if not t[1] in self.atom_dict:
                raise Exception("'%s' is not a known function." % t[1])
            atom = self.atom_dict[t[1]]
            # Check if missing arguments.
            (atom_str, missing_args) = get_atom_string(t[1], t[3])
            if missing_args:
                raise Exception("Missing arguments in '%s'." % atom_str)
            try:
                t[0] = atom(*t[3])
            except TypeError:
                raise Exception("Incorrect number of arguments in '%s'." % atom_str)

        # Catch all error for atomic function.
        def p_expression_atom_error(t):
            'expression : ID LPAREN error RPAREN'
            print t[3]
            atom_str = get_atom_string(t[1], [t[3]])
            raise Exception("Syntax error in '%s'." % atom_str)

        # List of expressions.
        # Single expression or STRING_ARG.
        def p_expression_list_single(t):
            '''expression_list : expression_or_empty
                               | STRING_ARG'''
            t[0] = [t[1]]

        # Concatenated expressions or STRING_ARGs.
        def p_expression_list_multi(t):
            '''expression_list : expression_list COMMA expression_or_empty
                               | expression_list COMMA STRING_ARG'''
            t[1].append(t[3])
            t[0] = t[1]

        # Error productions for expression lists with missing arguments.
        def p_expression_or_empty(t):
            '''expression_or_empty :
                                   | expression '''
            t[0] = '' if len(t) == 1 else t[1]

        # Unary plus and minus.
        def p_expression_uplus(t):
            'expression : PLUS expression %prec UPLUS'
            t[0] = t[2]

        def p_expression_uminus(t):
            'expression : MINUS expression %prec UMINUS'
            t[0] = -t[2]

        # Parenthesized expression.
        def p_expression_group(t):
            'expression : LPAREN expression RPAREN'
            t[2].add_parens()
            t[0] = t[2]

        # Raw number.
        def p_expression_number(t):
            '''expression : INT
                          | FLOAT'''
            t[0] = Constant(t[1])

        # Variable or parameter.
        def p_expression_id(t):
            'expression : ID'
            try:
                t[0] = self.symbol_table[t[1]]
            except LookupError:
                raise Exception("'%s' is not a known variable or parameter." % t[1])

        def p_error(t):
            raise Exception(ply.yacc.token())
            raise Exception("Missing ')' or other invalid syntax.")

        # Build the parser, tabmodule set so it loads parsetab.py
        return ply.yacc.yacc(tabmodule="dcp_parser.parsetab")