from dcp_parser.expression.vexity import Vexity

class Monotonicity(object):
    """ Monotonicity of atomic functions in a given argument. """
    INCREASING_KEY = 'INCREASING'
    DECREASING_KEY = 'DECREASING'
    NONMONOTONIC_KEY = 'NONMONOTONIC'

    MONOTONICITY_SET = set([INCREASING_KEY, DECREASING_KEY, NONMONOTONIC_KEY])

    def __init__(self,monotonicity_str):
        if monotonicity_str in Monotonicity.MONOTONICITY_SET:
            self.monotonicity_str = monotonicity_str
        else:
            raise Exception("No such monotonicity %s exists." % str(monotonicity_str))

    def __repr__(self):
        return "Monotonicity('%s')" % self.monotonicity_str
    
    def __str__(self):
        return self.monotonicity_str
    
    """
    Applies DCP composition rules to determine vexity in each argument.
    Composition rules:
        Key: Function vexity + monotonicity + argument vexity == vexity in argument
        anything + anything + constant == constant
        anything + anything + affine == original vexity
        convex/affine + increasing + convex == convex
        convex/affine + decreasing + concave == convex
        concave/affine + increasing + concave == concave
        concave/affine + decreasing + convex == concave
    Notes: Increasing (decreasing) means non-decreasing (non-increasing).
        Any combinations not covered by the rules result in a nonconvex expression.
    """
    def dcp_vexity(self, func_vexity, arg_vexity):
        if arg_vexity == Vexity.CONSTANT:
            return arg_vexity
        elif arg_vexity == Vexity.AFFINE:
            return func_vexity
        elif self.monotonicity_str == Monotonicity.INCREASING_KEY:
            return func_vexity + arg_vexity
        elif self.monotonicity_str == Monotonicity.DECREASING_KEY:
            return func_vexity - arg_vexity
        else: # non-monotonic
            return Vexity.NONCONVEX

# Class constants for all monotonicity types.
Monotonicity.INCREASING = Monotonicity(Monotonicity.INCREASING_KEY)
Monotonicity.DECREASING = Monotonicity(Monotonicity.DECREASING_KEY)
Monotonicity.NONMONOTONIC = Monotonicity(Monotonicity.NONMONOTONIC_KEY)