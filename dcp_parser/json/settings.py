from dcp_parser.expression.curvature import Curvature
from dcp_parser.expression.sign import Sign
from dcp_parser.atomic.monotonicity import Monotonicity

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
                str(Sign.UNKNOWN): 'unknown sign',
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
                'unknown sign': Sign.UNKNOWN,
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

PARENT_KEY = 'parent'
MONOTONICITY_KEY = 'monotonicity'
SHORT_NAME_KEY = 'short_name'

# Error keys
ERRORS_KEY = 'errors'
UNSORTED_ERRORS_KEY = 'unsorted_errors'
INDEXED_ERRORS_KEY = 'indexed_errors'