import settings
import dcp_parser.expression.settings as EXP_SET
from dcp_violation import DCPViolation
from dcp_parser.atomic.monotonicity import Monotonicity

class CompositionError(DCPViolation):
    """ Represents a DCP violation through function composition."""
    BASE_MSG = "Illegal composition:"

    def __init__(self, func_curvature, monotonicity, arg_curvature, arg_sign, index):
        self.func_curvature = func_curvature
        self.monotonicity = monotonicity
        self.arg_curvature = arg_curvature
        self.arg_sign = arg_sign
        self.index = index

    def __str__(self):
        error_str = " ".join([CompositionError.BASE_MSG, 
                              CompositionError.type_to_name(self.func_curvature),
                              CompositionError.type_to_name(self.monotonicity),
                              "with",
                              CompositionError.type_to_name(self.arg_curvature),
                              "argument"])
        return settings.DCP_ERROR_MSG + error_str