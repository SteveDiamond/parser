import json
import settings as s
from dcp_parser.expression.constraints import Constraint, EqConstraint, LeqConstraint, GeqConstraint
from expression_encoder import ExpressionEncoder
# Taken from http://docs.python.org/2/library/json.html

class ConstraintEncoder(json.JSONEncoder):
    """ Encodes a constraint as JSON """
    def default(self, obj):
        if isinstance(obj, Constraint):
            json_map = {
                        s.TYPE_KEY: s.CONSTRAINT_TYPE,
                        s.NAME_KEY: str(obj),
                        s.SHORT_NAME_KEY: obj.short_name,
                        s.CLASS_KEY: s.TYPE_TO_NAME[obj.__class__.__name__],
                       }
            # Encode the error as its string representation.
            # Save indexed errors in a map.
            error_map = {s.UNSORTED_ERRORS_KEY: [], s.INDEXED_ERRORS_KEY: {}}
            for error in obj.errors:
                if error.is_indexed():
                    error_map[s.INDEXED_ERRORS_KEY][error.index] = str(error)
                else:
                    error_map[s.UNSORTED_ERRORS_KEY].append(str(error))
            json_map[s.ERRORS_KEY] = error_map

            json_map[s.SUBEXP_KEY] = [ExpressionEncoder().default(sub) for sub in obj.subexpressions]
            return json_map
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

    # Translates JSON into a Constraint.
    # Used for testing. Does not preserve all information.
    @staticmethod
    def as_constraint(dct):
        # dct already parsed
        if isinstance(dct, Constraint):
            return dct
        subexpressions = [ExpressionEncoder.as_expression(sub) for sub in dct[s.SUBEXP_KEY]]
        lhs = subexpressions[0]
        rhs = subexpressions[1]
        constraint_str = dct[s.SHORT_NAME_KEY]
        if constraint_str == EqConstraint.CONSTRAINT_STR:
            constraint = EqConstraint(lhs,rhs)
        elif constraint_str == LeqConstraint.CONSTRAINT_STR:
            constraint = LeqConstraint(lhs,rhs)
        elif constraint_str == GeqConstraint.CONSTRAINT_STR:
            constraint = GeqConstraint(lhs,rhs)
        else:
            raise Exception("Invalid constraint type.")
        constraint.json_errors = dct[s.ERRORS_KEY]
        return constraint