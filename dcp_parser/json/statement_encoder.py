import json
import settings as s
from dcp_parser.expression.expression import Expression
from dcp_parser.expression.constraints import Constraint
from constraint_encoder import ConstraintEncoder
from expression_encoder import ExpressionEncoder
# Taken from http://docs.python.org/2/library/json.html

class StatementEncoder(json.JSONEncoder):
    """ Encodes a statement as JSON """
    def default(self, obj):
        if isinstance(obj, Constraint):
            return ConstraintEncoder().default(obj)
        elif isinstance(obj, Expression):
            return ExpressionEncoder().default(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

    # Translates JSON into a Statement.
    # Used for testing. Does not preserve all information.
    @staticmethod
    def as_statement(dct):
        if s.TYPE_KEY in dct:
            if dct[s.TYPE_KEY] == s.EXP_TYPE:
                return ExpressionEncoder.as_expression(dct)
            if dct[s.TYPE_KEY] == s.CONSTRAINT_TYPE:
                return ConstraintEncoder.as_constraint(dct)
        return dct