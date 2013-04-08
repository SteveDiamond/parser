# from utils import error_msg, id_wrapper, \
#     isunknown, ispositive, isnegative, \
#     isaff, iscvx, isccv, ismatrix, isscalar, isvector   
import settings
from sign import Sign
from curvature import Curvature
from sys import maxint
from numbers import Number
from dcp_parser.error_messages.dcp_violation import DCPViolation

class Expression(object):
    """
    A convex optimization expression.
    Records sign, curvature, string representation, and component expressions.
    The component expressions can be used to reconstruct the parse tree.

    Priority is the order of operations priority of the binary operation that
    created the expression (if any). It is used to reconstruct parentheses.
    """
    
    def __init__(self, curvature, sign, name, 
                 subexpressions = None, priority = maxint, errors = None):
        self.curvature = curvature
        self.sign = sign
        self.name = name
        self.subexpressions = subexpressions
        self.priority = priority
        self.errors = errors

    # Determines whether the subexpressions of a expression constructed
    # by a binary relation should be parenthesized.
    def impute_parens(self):
        # Lower priority operations that happened first
        # must have been parenthesized.
        # Likewise with equal priority operations to the right.
        exp = self.subexpressions[0]
        exp_str = str(exp)
        if exp.priority < self.priority:
            exp_str = "(" + exp_str + ")"
        self.name = exp_str + self.name

        exp = self.subexpressions[1]
        exp_str = str(exp)
        if exp.priority <= self.priority:
            exp_str = "(" + exp_str + ")"
        self.name = self.name + exp_str

    # Verifies that other in binary operations is a number or
    # an expression. If it is a number, it is converted to a constant.
    @staticmethod
    def type_check(other):
        if isinstance(other, Number):
            return Constant(other)
        elif isinstance(other, Expression):
            return other
        else:
            raise Exception("Illegal operation on object %s. Object must be of "
                            "type number or Expression, but is type %s."
                            % (str(other), other.__class__.__name__))
    
    def __add__(self, other):
        other = Expression.type_check(other)
        exp = Expression(self.curvature + other.curvature,
                          self.sign + other.sign,
                          settings.PLUS, 
                          [self,other],
                          settings.PRIORITY_MAP[settings.PLUS])
        exp.impute_parens()
        exp.errors = DCPViolation.operation_error(settings.PLUS, self, other, exp)
        return exp

    # Called if var + Expression not implemented, with arguments reversed.
    def __radd__(self, other):
        return settings.type_check(other) + self
    
    def __sub__(self, other):
        other = Expression.type_check(other)
        exp = Expression(self.curvature - other.curvature,
                          self.sign - other.sign,
                          settings.MINUS, 
                          [self,other],
                          settings.PRIORITY_MAP[settings.MINUS])
        exp.impute_parens()
        exp.errors = DCPViolation.operation_error(settings.MINUS, self, other, exp)
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
        other = Expression.type_check(other)
        sign = self.sign * other.sign
        curvature = self.curvature * other.curvature
        exp = Expression(curvature, 
                         sign, 
                         settings.MULT, 
                         [self,other],
                         settings.PRIORITY_MAP[settings.MULT])
        exp.sign_by_curvature()
        exp.impute_parens()
        exp.errors = DCPViolation.operation_error(settings.MULT, self, other, exp)
        return exp

    # Called if var * Expression not implemented, with arguments reversed.
    def __rmul__(self, other):
        return Expression.type_check(other) * self

    def __div__(self, other):
        other = Expression.type_check(other)
        sign = self.sign / other.sign
        curvature = self.curvature / other.curvature
        exp = Expression(curvature, 
                         sign, 
                         settings.DIV, 
                         [self,other],
                         settings.PRIORITY_MAP[settings.DIV])
        exp.sign_by_curvature()
        exp.impute_parens()
        exp.errors = DCPViolation.operation_error(settings.DIV, self, other, exp)
        return exp

    # Called if var / Expression not implemented, with arguments reversed.
    def __rdiv__(self, other):
        return Expression.type_check(other) / self
        
    def __neg__(self):
        return Expression(-self.curvature,
                          -self.sign,
                          '-' + str(self), 
                          [self])
    
    # def __le__(self,other):
    #     if iscvx(self) and isccv(other):
    #         return LeqConstraint(self,other)
    #     else:
    #         raise Exception("Cannot have '%s <= %s'" % (self.curvature_names[self.curvature], other.curvature_names[self.curvature]))
    
    # def __ge__(self,other):
    #     if isccv(self) and iscvx(other):
    #         return GeqConstraint(self,other)
    #     else:
    #         raise Exception("Cannot have '%s >= %s'" % (self.curvature_names[self.curvature], other.curvature_names[self.curvature]))
    
    # def __eq__(self,other):
    #     if isaff(self) and isaff(other):
    #         return EqConstraint(self,other)
    #     else:
    #         raise Exception("Cannot have '%s == %s'" % (self.curvature_names[self.curvature], other.curvature_names[self.curvature]))
            
    def __lt__(self, other): return NotImplemented
    def __gt__(self, other): return NotImplemented
    def __ne__(self, other): return NotImplemented
    
    def __repr__(self):
        """Representation in Python"""
        return "Expression(%s, %s, %s, %s)" % (self.curvature, 
                                               self.sign, 
                                               self.name, 
                                               self.subexpressions)
    
    def __str__(self):
        """String representation"""
        return self.name


class Variable(Expression):
    """ A convex optimization variable. """
    def __init__(self, name):
        super(Variable, self).__init__(Curvature.AFFINE,
                                       Sign.UNKNOWN,
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