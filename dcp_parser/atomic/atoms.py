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

    # Sign of argument to monoticity in that argument.
    # For all functions akin to |x|
    ABS_SIGN_TO_MONOTONICITY = {
                            str(Sign.POSITIVE): Monotonicity.INCREASING,
                            str(Sign.ZERO): Monotonicity.INCREASING,
                            str(Sign.NEGATIVE): Monotonicity.DECREASING,
                            str(Sign.UNKNOWN): Monotonicity.NONMONOTONIC
                            }

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

    # Returns argument signs as a list.
    def argument_signs(self):
        signs = []
        for arg in self.args:
            signs.append(arg.sign)
        return signs

    # Converts an Atom into an expression with the same curvature and sign.
    # Used for defining atoms as compositions of atoms.
    @staticmethod
    def atom_to_expression(instance):
        return Expression(instance.curvature(), instance.sign(), "no name", instance.arguments())

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
        monotonicity = Quad_over_lin.ABS_SIGN_TO_MONOTONICITY[arg_sign_str]
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
        # Throws error if argument is negative or zero.
        # TODO correct?
        super(Log, self).__init__(arg)
        sign = self.args[0].sign
        if sign == Sign.NEGATIVE or sign == Sign.ZERO:
            raise Exception('log only accepts positive arguments.')

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
        return Sign.sum(*signs)

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
    p defaults to 2.
    """
    def __init__(self, *args):
        # Set p to last arg if last arg is not an Expression
        # Otherwise default to p = 2
        p = 2
        if len(args) > 0 and not isinstance(args[len(args)-1],Expression):
            p = args[len(args)-1]
            args = args[:-1]
        # Throws error if p is invalid.
        if not ( (isinstance(p, Number) and p >= 1) or p == 'Inf'):
            raise Exception('Invalid p-norm, p = %s' % p)
        super(Norm,self).__init__(*args)

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
            monotonicity = Norm.ABS_SIGN_TO_MONOTONICITY[sign_str]
            monotonicities.append(monotonicity)
        return monotonicities

class Abs(Norm):
    """ Absolute value of one scalar argument. """
    def __init__(self, x):
        super(Abs,self).__init__(1,x)

class Entr(Atom):
    """ The entropy function -x*log(x) """
    def __init__(self, x):
        super(Entr,self).__init__(x)

    # Always UNKNOWN
    def sign(self):
        return Sign.UNKNOWN

    # Always concave
    def signed_curvature(self):
        return Curvature.CONCAVE

    # Always non-monotonic
    def monotonicity(self):
        return [Monotonicity.NONMONOTONIC]


class Huber(Atom):
    """ 
    The Huber function
    Huber(x,M) = 2M|x|-M^2 for |x| >= M
                 |x|^2 for |x| <= M
    M defaults to 1. M must be positive.
    """
    def __init__(self, x, M=1):
        # Throws error if p is invalid.
        if not (isinstance(M, Number) and M > 0):
            raise Exception('Invalid M for %s function, M = %s' \
                % (self.__class__.__name__.lower(), M))
        super(Huber,self).__init__(x)

    # Always positive
    def sign(self):
        return Sign.POSITIVE

    # Always convex
    def signed_curvature(self):
        return Curvature.CONVEX

    # Increasing (decreasing) for positive (negative) argument.
    def monotonicity(self):
        arg_sign_str = str(self.args[0].sign)
        monotonicity = Berhu.ABS_SIGN_TO_MONOTONICITY[arg_sign_str]
        return [monotonicity]

class Berhu(Huber):
    """ 
    The reversed Huber function
    Berhu(x,M) = |x| for |x| <= M
                 (|x|^2 + M^2)/2M for |x| >= M
    M defaults to 1. M must be positive.
    """

class Huber_pos(Huber):
    """ Same as Huber for non-negative x, zero for negative x. """
    # Positive unless x negative or zero, in which case zero.
    def sign(self):
        if self.args[0].sign <= Sign.ZERO:
            return Sign.ZERO
        else:
            return Sign.POSITIVE

    # Convex unless zero, in which case constant.
    def signed_curvature(self):
        if self.sign() <= Sign.ZERO:
            return Curvature.CONSTANT
        else:
            return Curvature.CONVEX

    # Always increasing.
    def monotonicity(self):
        return [Monotonicity.INCREASING]

class Huber_circ(Huber_pos):
    """
    Circularly symmetric Huber function
    Huber_circ(M, vector) is equivalent to huber_pos(norm(x),M)
    Default M is 1.
    """
    def __init__(self, *args):
        args = list(args)
        # Default to M=1 if last argument is not a number.
        M = 1 
        if len(args) > 0 and isinstance(args[len(args)-1],Number):
            M = args[len(args)-1]
            args = args[:-1]
        norm = Huber_circ.atom_to_expression(Norm(2,*args))
        super(Huber_circ, self).__init__(norm,M)

class Inv_pos(Atom):
    """ 1/max{x,0} """
    def __init__(self, x):
        super(Inv_pos, self).__init__(x)
        # Requires that x be non-zero and non-negative
        if x.sign <= Sign.ZERO:
            raise Exception("inv_pos only accepts positive arguments.")

    # Always positive
    def sign(self):
        return Sign.POSITIVE

    # Always convex
    def signed_curvature(self):
        return Curvature.CONVEX

    # Always decreasing.
    def monotonicity(self):
        return [Monotonicity.DECREASING]

class Kl_div(Atom):
    """ 
    Kullback-Leibler distance 
    kl_div(x,y) = x*log(x/y)-x+y
    Requires x,y non-negative and x == 0 iff y == 0
    """
    def __init__(self, x,y):
        super(Kl_div, self).__init__(x,y)
        # Requires that x,y be non-negative.
        if x.sign < Sign.ZERO or y.sign < Sign.ZERO:
            raise Exception("kl_div does not accept negative arguments.")
        elif Sign.min(x.sign, y.sign) == Sign.ZERO and x.sign != y.sign:
            raise Exception("kl_div(x,y) requires that x == 0 if and only if y == 0.")

    # Always unknown
    def sign(self):
        return Sign.UNKNOWN

    # Always convex
    def signed_curvature(self):
        return Curvature.CONVEX

    # Always non-monotonic.
    def monotonicity(self):
        return [Monotonicity.NONMONOTONIC] * len(self.args)

class Norm_largest(Atom):
    """ 
    Sum of the k largest elements.
    norm_largest(vector, k) 
    """
    def __init__(self, *args):
        args = list(args)
        # Use last argument as k
        last_index = len(args)-1
        if len(args) > 0 and isinstance(args[last_index],Number):
            k = args[last_index]
            args = args[:-1]
            super(Norm_largest, self).__init__(*args)
        else:
            raise Exception("Invalid value for k in norm_largest(*vector,k).")

    # Always unknown
    # Could determine from signs of elements, but would be obscure.
    def sign(self):
        return Sign.UNKNOWN

    # Always convex
    def signed_curvature(self):
        return Curvature.CONVEX

    # Increasing (decreasing) for positive (negative) argument.
    def monotonicity(self):
        monotonicities = []
        for scalar in self.args:
            sign_str = str(scalar.sign)
            monotonicity = Norm_largest.ABS_SIGN_TO_MONOTONICITY[sign_str]
            monotonicities.append(monotonicity)
        return monotonicities

class Pos(Atom):
    """ max{x,0} """
    def __init__(self, x):
        super(Pos, self).__init__(x)

    # Positive unless x negative or zero, in which case zero.
    def sign(self):
        if self.args[0].sign <= Sign.ZERO:
            return Sign.ZERO
        else:
            return Sign.POSITIVE

    # Convex unless zero, in which case constant.
    def signed_curvature(self):
        if self.sign() <= Sign.ZERO:
            return Curvature.CONSTANT
        else:
            return Curvature.CONVEX

    # Always increasing.
    def monotonicity(self):
        return [Monotonicity.INCREASING]

class Pow_p(Atom):
    """ 
    pow_pos(x,p)
    If p <= 0 then x^p if x > 0, else +Inf
    If 0 < p <=1 then x^p if x >= 0, else -Inf
    If p < 1 then x^p if x >= 0, else +Inf
    """
    def __init__(self,x,p):
        if not isinstance(p, Number):
            raise Exception('Invalid p for pow_p(x,p), p = %s.' % p)
        self.p = p
        super(Pow_p, self).__init__(x)
        self.x = self.args[0]

    # Depends on p and the sign of x
    def sign(self):
        if self.p <= 0:
            return Sign.POSITIVE
        elif self.p <= 1:
            return Sign.min(Sign.POSITIVE, self.x.sign)
        else: # p > 1
            return Sign.POSITIVE

    # Depends on p.
    def signed_curvature(self):
        if self.p <= 0:
            return Curvature.CONVEX
        elif self.p <= 1:
            return Curvature.CONCAVE
        else: # p > 1
            return Curvature.CONVEX

    # Depends on p and the sign of x.
    def monotonicity(self):
        if self.p <= 0:
            return [Monotonicity.DECREASING]
        elif self.p <= 1:
            return [Monotonicity.INCREASING]
        else: # p > 1
            return [Pow_p.ABS_SIGN_TO_MONOTONICITY[str(self.x.sign)]]

class Pow_abs(Pow_p):
    """ |x|^p """
    def __init__(self,x,p):
        # Must have p >= 1
        if not (isinstance(p, Number) and p >= 1):
            raise Exception('Must have p >= 1 for pow_abs(x,p), but have p = %s.' % p)
        Pow_abs.atom_to_expression(Abs(x))
        super(Pow_abs, self).__init__(x,p)

