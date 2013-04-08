import abc
from dcp_parser.expression.curvature import Curvature
from dcp_parser.atomic.monotonicity import Monotonicity

class DCPViolation(object):
    """ Abstract base class for DCP Violations. """
    __metaclass__ = abc.ABCMeta

    # Maps curvature and monotonicity to the error message name.
    TYPE_TO_NAME = {
                str(Curvature.CONSTANT): 'constant',
                str(Curvature.AFFINE): 'affine',
                str(Curvature.CONVEX): 'convex',
                str(Curvature.CONCAVE): 'concave',
                str(Curvature.NONCONVEX): 'non-convex',
                str(Monotonicity.INCREASING): 'non-decreasing',
                str(Monotonicity.DECREASING): 'non-increasing',
                str(Monotonicity.NONMONOTONIC): 'non-monotonic',
                }

    # Maps curvature and monotonicity to the error message name.
    @staticmethod
    def type_to_name(type):
        return DCPViolation.TYPE_TO_NAME[str(type)]