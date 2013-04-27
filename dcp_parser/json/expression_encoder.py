import json
import settings as s
from dcp_parser.expression.expression import Expression
# Taken from http://docs.python.org/2/library/json.html

class ExpressionEncoder(json.JSONEncoder):
    """ Encodes an expression as JSON """
    def default(self, obj):
        if isinstance(obj, Expression):
            json_map = {
                        s.TYPE_KEY: s.EXP_TYPE,
                        s.NAME_KEY: str(obj),
                        s.SHORT_NAME_KEY: obj.short_name,
                        s.CURVATURE_KEY: s.TYPE_TO_NAME[str(obj.curvature)],
                        s.SIGN_KEY: s.TYPE_TO_NAME[str(obj.sign)],
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

            json_map[s.SUBEXP_KEY] = [self.default(sub) for sub in obj.subexpressions]
            # Ignore monotonicity if None (i.e. not an atomic function)
            if obj.monotonicity is not None:
                json_map[s.MONOTONICITY_KEY] = [s.TYPE_TO_NAME[str(tonicity)]
                                            for tonicity in obj.monotonicity]
            return json_map
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

    # Translates JSON into an Expression.
    # Used for testing. Does not preserve all information.
    @staticmethod
    def as_expression(dct):
        # dct already parsed
        if isinstance(dct, Expression):
            return dct
        curvature = s.NAME_TO_TYPE[dct[s.CURVATURE_KEY]]
        sign = s.NAME_TO_TYPE[dct[s.SIGN_KEY]]
        name = dct[s.NAME_KEY]
        subexpressions = [ExpressionEncoder.as_expression(sub) for sub in dct[s.SUBEXP_KEY]]
        monotonicity = None
        if s.MONOTONICITY_KEY in dct:
            monotonicity = [s.NAME_TO_TYPE[tonicity] for tonicity in dct[s.MONOTONICITY_KEY]]
        short_name = dct[s.SHORT_NAME_KEY]
        exp = Expression(curvature, sign, name, subexpressions, 
                          monotonicity=monotonicity, short_name=short_name)
        exp.json_errors = dct[s.ERRORS_KEY]
        return exp