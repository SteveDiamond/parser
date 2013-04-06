""" Definitions of atomic functions """
import abc
from dcp_parser.expression.sign import Sign
from dcp_parser.expression.vexity import Vexity
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

    # Determines vexity from args and sign.
    def vexity(self):
        vexity = self.signed_vexity(self.sign())
        return Atom.dcp_vexity(vexity, self.args, self.monotonicity())

    # Determines vexity from sign, e.g. x^3 is convex for positive x
    # and concave for negative x.
    # Usually result will not depend on sign.
    @abc.abstractmethod
    def signed_vexity(self, sign):
        return NotImplemented

    # Returns a list with the monotonicity in each argument.
    # Montonicity can depend on the sign of the argument.
    @abc.abstractmethod
    def monotonicity(self):
        return NotImplemented

    """
    Applies DCP composition rules to determine vexity in each argument.
    The overall vexity is the sum of the argument vexities.
    """
    @staticmethod
    def dcp_vexity(vexity, args, monotonicities):
        if len(args) == 0 or len(args) != len(monotonicities):
            raise Exception('The number of args must be non-zero and'
                            ' equal to the number of monotonicities.')
        arg_vexities = []
        for i in range(len(args)):
            monotonicity = monotonicities[i]
            arg = args[i]
            arg_vexities.append(monotonicity.dcp_vexity(vexity, arg.vexity))
        final_vexity = arg_vexities[0]
        for vex in arg_vexities:
            final_vexity = final_vexity + vex
        return final_vexity

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
    def signed_vexity(self, sign):
        return Vexity.CONVEX

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
    def signed_vexity(self, sign):
        return Vexity.CONVEX

    # Always increasing.
    def monotonicity(self):
        return [Monotonicity.INCREASING] * len(self.args)

class Max(Atom):
    """ Maximum argument. """
    # Positive if any arg positive, unknown if any arg unknown,
    # negative if all arguments negative, zero if at least 
    # one arg zero and all others negative.
    def sign(self):
        zero_arg = False
        for arg in self.args:
            if arg.sign == Sign.POSITIVE or arg.sign == Sign.UNKNOWN:
                return arg.sign
            elif arg.sign == Sign.ZERO:
                zero_arg = True
        if zero_arg: 
            return Sign.ZERO 
        else: 
            return Sign.NEGATIVE

    # Always convex
    def signed_vexity(self, sign):
        return Vexity.CONVEX

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
    def signed_vexity(self, sign):
        return Vexity.CONCAVE

    # Always increasing.
    def monotonicity(self):
        return [Monotonicity.INCREASING]
