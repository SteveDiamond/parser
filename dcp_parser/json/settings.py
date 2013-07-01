from dcp_parser.expression.curvature import Curvature
from dcp_parser.expression.sign import Sign
from dcp_parser.atomic.monotonicity import Monotonicity
from dcp_parser.expression.constraints import Constraint, EqConstraint, LeqConstraint, GeqConstraint
from dcp_parser.expression.expression import Expression, Variable, Parameter, Constant

# Maps curvature, monotonicity, and sign to the JSON name.
TYPE_TO_NAME = {
                str(Curvature.CONSTANT): 'constant',
                str(Curvature.AFFINE): 'affine',
                str(Curvature.CONVEX): 'convex',
                str(Curvature.CONCAVE): 'concave',
                str(Curvature.NONCONVEX): 'non-convex',
                str(Monotonicity.INCREASING): 'non-decreasing',
                str(Monotonicity.DECREASING): 'non-increasing',
                str(Monotonicity.NONMONOTONIC): 'non-monotonic',
                str(Sign.POSITIVE): 'positive',
                str(Sign.NEGATIVE): 'negative',
                str(Sign.ZERO): 'zero',
                str(Sign.UNKNOWN): 'unknown',
                # Class names
                EqConstraint.__name__: Constraint.__name__,
                LeqConstraint.__name__: Constraint.__name__,
                GeqConstraint.__name__: Constraint.__name__,
                Expression.__name__: 'Function',
                Variable.__name__: Variable.__name__,
                Parameter.__name__: Parameter.__name__,
                Constant.__name__: Constant.__name__,
               }

# Maps JSON name to curvature, sign, or monotonicity object.
NAME_TO_TYPE = {
                'constant': Curvature.CONSTANT,
                'affine': Curvature.AFFINE,
                'convex': Curvature.CONVEX,
                'concave': Curvature.CONCAVE,
                'non-convex': Curvature.NONCONVEX,
                'non-decreasing': Monotonicity.INCREASING,
                'non-increasing': Monotonicity.DECREASING,
                'non-monotonic': Monotonicity.NONMONOTONIC,
                'positive': Sign.POSITIVE,
                'negative': Sign.NEGATIVE,
                'zero': Sign.ZERO,
                'unknown': Sign.UNKNOWN,
               }

# Type keys and values
TYPE_KEY = 'type'
EXP_TYPE = 'Expression'
CONSTRAINT_TYPE = 'Constraint'

# Strings for keys
SIGN_KEY = 'sign'
CURVATURE_KEY = 'curvature'
NAME_KEY = 'name'
SUBEXP_KEY = 'children'
PRIORITY_KEY = 'priority'
CLASS_KEY = 'class'

MONOTONICITY_KEY = 'monotonicity'
SHORT_NAME_KEY = 'short_name'

# Error keys
ERRORS_KEY = 'errors'
UNSORTED_ERRORS_KEY = 'unsorted_errors'
INDEXED_ERRORS_KEY = 'indexed_errors'