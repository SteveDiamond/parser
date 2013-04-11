""" Definitions of atomic functions """
import abc
from numbers import Number
from dcp_parser.expression.sign import Sign
from dcp_parser.expression.curvature import Curvature
from dcp_parser.atomic.monotonicity import Monotonicity
from dcp_parser.expression.expression import Expression

class Atom(object):
    """ Abstract base class for all atoms. """
    __metaclass__ = abc.ABCMeta

    # args is the subclass instance followed by expressions.
    def __init__(self, *args):
        # Convert numeric constants to Constants
        self.args = map(Expression.type_check, list(args))

    # Returns expression arguments.
    def arguments(self):
        return self.args

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
    The overall curvature is the sum of the argument curvatures.
    """
    @staticmethod
    def dcp_curvature(curvature, args, monotonicities):
        if len(args) == 0 or len(args) != len(monotonicities):
            raise Exception('The number of args must be non-zero and'
                            ' equal to the number of monotonicities.')
        arg_curvatures = []
        for i in range(len(args)):
            monotonicity = monotonicities[i]
            arg = args[i]
            arg_curvatures.append(monotonicity.dcp_curvature(curvature, arg.curvature))

        return Curvature.sum(arg_curvatures)

"""---------------------------------- Atoms ----------------------------------"""
class Quad_over_lin(Atom):
    """ x^2/y """
    # Sign of first argument to monotonicity in first argument.
    SIGN_TO_MONOTONICITY = {
                            str(Sign.POSITIVE): Monotonicity.INCREASING,
                            str(Sign.ZERO): Monotonicity.INCREASING,
                            str(Sign.NEGATIVE): Monotonicity.DECREASING,
                            str(Sign.UNKNOWN): Monotonicity.NONMONOTONIC
                            }

    def __init__(self, x, y):
        super(Quad_over_lin,self).__init__(x, y)
        # Throws error if argument is negative or zero.
        sign = self.args[1].sign
        if sign == Sign.NEGATIVE or sign == Sign.ZERO:
            raise Exception('Quad_over_lin only accepts positive second arguments.')

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
        return [monotonicity, Monotonicity.DECREASING]

class Square(Quad_over_lin):
    """ Squares a single argument. """
    def __init__(self, x):
        super(Square,self).__init__(x,1)

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
    # Negative if all arguments negative.
    # Zero if at least one arg zero and all others negative.
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

class Min(Atom):
    """ Minimum argument. """
    # Negative if any arg negative.
    # Zero if no args negative and any arg zero.
    # Unknown if at least one arg unknown and all others positive.
    # Positive if all args positive.
    def sign(self):
        smallest = Sign.POSITIVE
        for arg in self.args:
            if arg.sign < smallest:
                smallest = arg.sign
        return smallest

    # Always convex
    def signed_curvature(self):
        return Curvature.CONCAVE

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

class Sum(Atom):
    """ Sum of all arguments. """
    # Sum of argument signs.
    def sign(self):
        signs = [arg.sign for arg in self.args]
        return Sign.sum(signs)

    # Always affine
    def signed_curvature(self):
        return Curvature.AFFINE

    # Always increasing.
    def monotonicity(self):
        return [Monotonicity.INCREASING] * len(self.args)

class Geo_mean(Atom):
    """ (x1*...*xn)^(1/n) """
    def __init__(self, *args):
        super(Geo_mean, self).__init__(*args)
        # Throws error if any argument is negative.
        for arg in self.args:
            if arg.sign == Sign.NEGATIVE:
                raise Exception('geo_mean does not accept negative arguments.')

    # Always positive
    def sign(self):
        return Sign.POSITIVE

    # Always concave
    def signed_curvature(self):
        return Curvature.CONCAVE

    # Always increasing.
    def monotonicity(self):
        return [Monotonicity.INCREASING] * len(self.args)

class Sqrt(Geo_mean):
    """ square root of a single argument """
    def __init__(self, x):
        super(Sqrt,self).__init__(x)

class Log_normcdf(Atom):
    """ 
    logarithm of cumulative distribution function of 
    standard normal random variable 
    """
    def __init__(self, x):
        super(Log_normcdf,self).__init__(x)

    # Always unknown
    def sign(self):
        return Sign.UNKNOWN

    # Always concave
    def signed_curvature(self):
        return Curvature.CONCAVE

    # Always increasing.
    def monotonicity(self):
        return [Monotonicity.INCREASING]

class Exp(Atom):
    """ e^x """
    def __init__(self, x):
        super(Exp,self).__init__(x)

    # Always positive
    def sign(self):
        return Sign.POSITIVE

    # Always convex
    def signed_curvature(self):
        return Curvature.CONVEX

    # Always increasing.
    def monotonicity(self):
        return [Monotonicity.INCREASING]

class Norm(Atom):
    """ 
    The p-norm for a vector (list of scalar values)
    Use:  Norm(p, *args)
    p can be either a number greater than or equal to 1 or 'Inf'
    """
    # Sign of first argument to monotonicity in first argument.
    SIGN_TO_MONOTONICITY = {
                            str(Sign.POSITIVE): Monotonicity.INCREASING,
                            str(Sign.ZERO): Monotonicity.INCREASING,
                            str(Sign.NEGATIVE): Monotonicity.DECREASING,
                            str(Sign.UNKNOWN): Monotonicity.NONMONOTONIC
                            }

    def __init__(self, p, *vector):
        super(Norm,self).__init__(*vector)
        # Throws error if p is invalid.
        if not ( (isinstance(p, Number) and p >= 1) or p == 'Inf'):
            raise Exception('Invalid Norm %s' % p)

    # Always positive
    def sign(self):
        return Sign.POSITIVE

    # Always convex
    def signed_curvature(self):
        return Curvature.CONVEX

    # Increasing (decreasing) for positive (negative) argument.
    def monotonicity(self):
        monotonicities = []
        for scalar in self.args:
            sign_str = str(scalar.sign)
            monotonicity = Norm.SIGN_TO_MONOTONICITY[sign_str]
            monotonicities.append(monotonicity)
        return monotonicities

class Abs(Norm):
    """ Absolute value of one scalar argument. """
    def __init__(self, x):
        super(Abs,self).__init__(1,x)


