from dcp_parser.expression.curvature import Curvature
from dcp_parser.expression.sign import Sign
from dcp_parser.atomic.monotonicity import Monotonicity
from operation_error import OperationError
from composition_error import CompositionError

class DCPViolationFactory(object):
    """ Factory class for OperationError and CompositionError. """

    # Returns an OperationError if the operation resulted in 
    # a non-convex expression.
    @staticmethod
    def operation_error(op_str, lh_exp, rh_exp, result_exp):
        if result_exp.curvature == Curvature.NONCONVEX:
            return [OperationError(op_str, lh_exp, rh_exp)]
        else:
            return []

    # Returns a list with a CompositionError for each argument that 
    # violates DCP composition rules, i.e. produces a non-convex composition.
    @staticmethod
    def composition_error(func_curvature, func_monotonicities, arg_curvatures):
        errors = []
        for i in range(len(func_monotonicities)):
            monotonicity = func_monotonicities[i]
            curvature = monotonicity.dcp_curvature(func_curvature, arg_curvatures[i])
            if curvature == Curvature.NONCONVEX:
                err = CompositionError(func_curvature, monotonicity, arg_curvatures[i], i)
                errors.append(err)

        if len(errors) == 0:
            return []
        else:
            return errors