# from utils import error_msg, id_wrapper, \
#     isunknown, ispositive, isnegative, \
#     isaff, iscvx, isccv, ismatrix, isscalar, isvector   
import settings
from sign import Sign
from curvature import Curvature
from sys import maxint
from numbers import Number
from statement import Statement
from constraints import EqConstraint, GeqConstraint, LeqConstraint
from dcp_parser.error_messages.dcp_violation_factory import DCPViolationFactory

class Expression(Statement):
    """
    A convex optimization expression.
    Records sign, curvature, string representation, and component expressions.
    The component expressions can be used to reconstruct the parse tree.

    Priority is the order of operations priority of the binary operation that
    created the expression (if any). It is used to reconstruct parentheses.

    Errors records the DCP violations introduced by forming the expression.
    Monotonicity stores the monotonicity in each argument for atomic functions.
    short_name is the name without the subexpressions, i.e. "x + y" is "+".
    """

    def __init__(self, curvature, sign, name, 
                 subexpressions = [],
                 errors = [],
                 monotonicity = None,
                 short_name = None): 
        self.curvature = curvature
        self.sign = sign
        self.name = name
        self.monotonicity = monotonicity
        # If no short_name given, default to the full name.
        if short_name is None:
            short_name = self.name
        super(Expression, self).__init__(short_name, subexpressions, errors)

    # Adds parentheses around the string representation of the expression.
    def add_parens(self):
        self.name = "(" + self.name + ")"

    # Verifies that expression is a number or an expression. 
    # If it is a number, it is converted to a constant.
    @staticmethod
    def type_check(expression):
        if isinstance(expression, Number):
            return Constant(expression)
        elif isinstance(expression, Expression):
            return expression
        else:
            raise Exception("Illegal operation on object %s. Object must be of "
                            "type number or Expression, but is type %s."
                            % (str(expression), expression.__class__.__name__))
    
    def __add__(self, other):
        exp = Expression(self.curvature + other.curvature,
                          self.sign + other.sign,
                          "%s %s %s" % (self.name, settings.PLUS, other.name),
                          [self,other],
                          short_name = settings.PLUS)
        exp.errors = DCPViolationFactory.operation_error(settings.PLUS, self, other, exp)
        return exp

    # Called if var + Expression not implemented, with arguments reversed.
    def __radd__(self, other):
        return settings.type_check(other) + self
    
    def __sub__(self, other):
        exp = Expression(self.curvature - other.curvature,
                          self.sign - other.sign,
                          "%s %s %s" % (self.name, settings.MINUS, other.name),
                          [self,other],
                          short_name = settings.MINUS)
        exp.errors = DCPViolationFactory.operation_error(settings.MINUS, self, other, exp)
        return exp

    # Called if var - Expression not implemented, with arguments reversed.
    def __rsub__(self, other):
        return Expression.type_check(other) - self

    # Adjust curvature based on sign of subexpressions.
    # Used for multiplication and division.
    # Only constant expressions can change the curvature,
    # e.g. negative constant * convex == concave
    # For multiplication by non-constants, the curvature
    # is always nonconvex.
    def sign_by_curvature(self):
        for i in range(len(self.subexpressions)):
            curvature = self.subexpressions[i].curvature
            sign = self.subexpressions[i].sign
            if curvature == Curvature.CONSTANT:
                self.curvature = self.curvature.sign_mult(sign)

    def __mul__(self, other):
        sign = self.sign * other.sign
        curvature = self.curvature * other.curvature
        exp = Expression(curvature, 
                         sign, 
                         "%s %s %s" % (self.name, settings.MULT, other.name),
                         [self,other],
                         short_name = settings.MULT)
        exp.sign_by_curvature()
        exp.errors = DCPViolationFactory.operation_error(settings.MULT, self, other, exp)
        return exp

    # Called if var * Expression not implemented, with arguments reversed.
    def __rmul__(self, other):
        return Expression.type_check(other) * self

    def __div__(self, other):
        sign = self.sign / other.sign
        curvature = self.curvature / other.curvature
        exp = Expression(curvature, 
                         sign, 
                         "%s %s %s" % (self.name, settings.DIV, other.name),
                         [self,other],
                         short_name = settings.DIV)
        exp.sign_by_curvature()
        exp.errors = DCPViolationFactory.operation_error(settings.DIV, self, other, exp)
        return exp

    # Called if var / Expression not implemented, with arguments reversed.
    def __rdiv__(self, other):
        return Expression.type_check(other) / self
        
    def __neg__(self):
        self = Expression.type_check(self)
        return Expression(-self.curvature,
                          -self.sign,
                          '-' + str(self), 
                          [self],
                          short_name = settings.MINUS)
    
    def __le__(self,other):
        return LeqConstraint(self, Expression.type_check(other))
    
    def __ge__(self,other):
        return GeqConstraint(self, Expression.type_check(other))
           
    def __eq__(self,other):
        return EqConstraint(self, Expression.type_check(other))
           
    def __repr__(self):
        """Representation in Python"""
        return "Expression(%s, %s, %s, %s, %s, %s, %s)" % (self.curvature,
                                                           self.sign, 
                                                           self.name, 
                                                           self.subexpressions,
                                                           self.errors,
                                                           self.monotonicity,
                                                           self.short_name)
    
    def __str__(self):
        """String representation"""
        return self.name


class Variable(Expression):
    """ A convex optimization variable. """
    def __init__(self, name, sign=Sign.UNKNOWN):
        super(Variable, self).__init__(Curvature.AFFINE,
                                       sign,
                                       name)
    
    def __repr__(self):
        return "Variable(%s)" % (self.name)

    def __str__(self):
        return self.name

        
class Parameter(Expression):
    """ A convex optimization parameter. """
    def __init__(self, name, sign):
        super(Parameter, self).__init__(Curvature.CONSTANT,
                                        sign,
                                        name)      
    def __repr__(self):
        return "Parameter(%s, %s)" % (self.name, self.sign)
            
    def __str__(self):
        return self.name
    
        
class Constant(Expression):
    def __init__(self, value):
        if value > 0:
            sign_str = Sign.POSITIVE_KEY
        elif value == 0:
            sign_str = Sign.ZERO_KEY
        else:
            sign_str = Sign.NEGATIVE_KEY
        super(Constant, self).__init__(Curvature.CONSTANT, 
                                       Sign(sign_str),
                                       str(value))
        
    def __repr__(self):
        return "Constant(%s)" % self.name