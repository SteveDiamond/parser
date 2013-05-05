import dcp_parser.expression.settings as EXP_SET
from dcp_violation import DCPViolation
from dcp_parser.expression.curvature import Curvature
from dcp_parser.expression.sign import Sign

class OperationError(DCPViolation):
    """ Represents a DCP violation through arithmetic operations. """
    BASE_MSG = "Illegal operation: "

    def __init__(self, op_str, lh_exp, rh_exp):
        self.op_str = op_str
        self.lh_exp = lh_exp
        self.rh_exp = rh_exp

    # Generates the appropriate error message given the curvature of the
    # lefthand and righthand expressions.
    def generate_error_str(self):
        lh_str = OperationError.type_to_name(self.lh_exp.curvature)
        rh_str = OperationError.type_to_name(self.rh_exp.curvature)

        # Sign can cause an error when a constant with unknown sign is
        # multiplied by or divides a convex or concave expression.
        # Otherwise sign does not matter.
        if self.op_str == EXP_SET.MULT:
            if OperationError.unknown_constant_error(self.lh_exp, self.rh_exp):
                lh_str = lh_str + " with unknown sign"
            elif OperationError.unknown_constant_error(self.rh_exp, self.lh_exp):
                rh_str = rh_str + " with unknown sign"
        if self.op_str == EXP_SET.DIV and \
            OperationError.unknown_constant_error(self.rh_exp, self.lh_exp):
            rh_str = rh_str + " with unknown sign"

        return (lh_str, rh_str)

    # Checks if lefthand is an unknown constant and right hand is convex or concave.
    @staticmethod
    def unknown_constant_error(const_exp, rh_exp):
        return const_exp.curvature == Curvature.CONSTANT and \
               const_exp.sign == Sign.UNKNOWN and \
               (rh_exp.curvature == Curvature.CONVEX or \
                rh_exp.curvature == Curvature.CONCAVE)

    # Core error message
    def error_message(self):
        (lh_str, rh_str) = self.generate_error_str()
        return "%s%s %s %s" % (OperationError.BASE_MSG, lh_str, self.op_str, rh_str)