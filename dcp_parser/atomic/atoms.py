""" Definitions of atomic functions """
import abc
from numbers import Number
from dcp_parser.expression.sign import Sign
from dcp_parser.expression.curvature import Curvature
from dcp_parser.atomic.monotonicity import Monotonicity

class Atom(object):
    """ Abstract base class for all atoms. """
    __metaclass__ = abc.ABCMeta

    # args is the subclass instance followed by expressions.
    def __init__(self, *args):
        self.args = list(args)

    # Determines sign from args.
    @abc.abstractmethod
    def sign(self):
        return NotImplemented

    # Determines curvature from args and sign.
    def curvature(self):
        curvature = self.signed_curvature()
        return Atom.dcp_curvature(curvature, self.args, self.monotonicity())

    # Returns argument curvatures as a list.
    def argument_curvatures(self):
        curvatures = []
        for arg in self.args:
            curvatures.append(arg.curvature)
        return curvatures

    # Determines curvature from sign, e.g. x^3 is convex for positive x
    # and concave for negative x.
    # Usually result will not depend on sign.
    @abc.abstractmethod
    def signed_curvature(self):
        return NotImplemented

    # Returns a list with the monotonicity in each argument.
    # Monotonicity can depend on the sign of the argument.
    @abc.abstractmethod
    def monotonicity(self):
        return NotImplemented

    """
    Applies DCP composition rules to determine curvature in each argument.
    The overall curvature is the sum of the argument vexities.
    """
    @staticmethod
    def dcp_curvature(curvature, args, monotonicities):
        if len(args) == 0 or len(args) != len(monotonicities):
            raise Exception('The number of args must be non-zero and'
                            ' equal to the number of monotonicities.')
        arg_vexities = []
        for i in range(len(args)):
            monotonicity = monotonicities[i]
            arg = args[i]
            arg_vexities.append(monotonicity.dcp_curvature(curvature, arg.curvature))
        final_curvature = arg_vexities[0]
        for vex in arg_vexities:
            final_curvature = final_curvature + vex
        return final_curvature

class Square(Atom):
    """ Squares a single argument. """
    SIGN_TO_MONOTONICITY = {
                            str(Sign.POSITIVE): Monotonicity.INCREASING,
                            str(Sign.ZERO): Monotonicity.INCREASING,
                            str(Sign.NEGATIVE): Monotonicity.DECREASING,
                            str(Sign.UNKNOWN): Monotonicity.NONMONOTONIC
                            }

    def __init__(self, arg):
        super(Square,self).__init__(arg)

    # Always positive
    def sign(self):
        return Sign.POSITIVE

    # Always convex
    def signed_curvature(self):
        return Curvature.CONVEX

    # Increasing (decreasing) for positive (negative) argument.
    def monotonicity(self):
        arg_sign_str = str(self.args[0].sign)
        monotonicity = Square.SIGN_TO_MONOTONICITY[arg_sign_str]
        return [monotonicity]

class Log_sum_exp(Atom):
    """ log(e^(arg[0]) + e^(arg[1]) + ... + e^(arg[n])) """
    # Always unknown
    def sign(self):
        return Sign.UNKNOWN

    # Always convex
    def signed_curvature(self):
        return Curvature.CONVEX

    # Always increasing.
    def monotonicity(self):
        return [Monotonicity.INCREASING] * len(self.args)

class Max(Atom):
    """ Maximum argument. """
    # Positive if any arg positive.
    # Unknown if no args positive and any arg unknown.
    # Negative if all arguments negative, zero if at least 
    # one arg zero and all others negative.
    def sign(self):
        largest = Sign.NEGATIVE
        for arg in self.args:
            if arg.sign > largest:
                largest = arg.sign
        return largest

    # Always convex
    def signed_curvature(self):
        return Curvature.CONVEX

    # Always increasing.
    def monotonicity(self):
        return [Monotonicity.INCREASING] * len(self.args)

class Log(Atom):
    """ Natural logarithm """
    def __init__(self, arg):
        super(Log, self).__init__(arg)
        # Throws error if argument is negative or zero.
        sign = self.args[0].sign
        if sign == Sign.NEGATIVE or sign == Sign.ZERO:
            raise Exception('Log only accepts positive arguments.')

    # Always unknown.
    def sign(self):
        return Sign.UNKNOWN

    # Always concave
    def signed_curvature(self):
        return Curvature.CONCAVE

    # Always increasing.
    def monotonicity(self):
        return [Monotonicity.INCREASING]