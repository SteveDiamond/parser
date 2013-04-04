# from utils import error_msg, id_wrapper, \
#     isunknown, ispositive, isnegative, \
#     isaff, iscvx, isccv, ismatrix, isscalar, isvector   
from sign import Sign
from vexity import Vexity
from sys import maxint

class Expression(object):
    """
    A convex optimization expression.
    Records sign, vexity, string representation, and component expressions.
    The component expressions can be used to reconstruct the parse tree.

    Priority is the order of operations priority of the binary operation that
    created the expression (if any). It is used to reconstruct parentheses.
    """

    # Constants for computing priority.
    MULT = ' * '
    DIV = ' / '
    PLUS = ' + '
    MINUS = ' - '
    PRIORITY_MAP = {MULT: 2, DIV: 2, PLUS: 1, MINUS: 1}
    
    def __init__(self, vexity, sign, name, subexpressions, priority = maxint):
        self.vexity = vexity
        self.sign = sign
        self.name = name
        self.subexpressions = subexpressions
        self.priority = priority

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
    
    def __add__(self, other):
        exp = Expression(self.vexity + other.vexity,
                          self.sign + other.sign,
                          Expression.PLUS, 
                          [self,other],
                          Expression.PRIORITY_MAP[Expression.PLUS])
        exp.impute_parens()
        return exp
    
    def __sub__(self, other):
        exp = Expression(self.vexity - other.vexity,
                          self.sign - other.sign,
                          Expression.MINUS, 
                          [self,other],
                          Expression.PRIORITY_MAP[Expression.MINUS])
        exp.impute_parens()
        return exp

    # Adjust vexity based on sign of subexpressions.
    # Used for multiplication and division.
    # Only constant expressions can change the vexity,
    # e.g. negative constant * convex == concave
    # For multiplication by non-constants, the vexity
    # is always nonconvex.
    def sign_by_vexity(self):
        for i in range(len(self.subexpressions)):
            vexity = self.subexpressions[i].vexity
            sign = self.subexpressions[i].sign
            if vexity == Vexity(Vexity.CONSTANT_KEY):
                self.vexity = self.vexity.sign_mult(sign)

    def __mul__(self, other):
        sign = self.sign * other.sign
        vexity = self.vexity * other.vexity
        exp = Expression(vexity, 
                         sign, 
                         Expression.MULT, 
                         [self,other],
                         Expression.PRIORITY_MAP[Expression.MULT])
        exp.sign_by_vexity()
        exp.impute_parens()
        return exp

    def __div__(self, other):
        sign = self.sign / other.sign
        vexity = self.vexity / other.vexity
        exp = Expression(vexity, 
                         sign, 
                         Expression.DIV, 
                         [self,other],
                         Expression.PRIORITY_MAP[Expression.DIV])
        exp.sign_by_vexity()
        exp.impute_parens()
        return exp
        
    def __neg__(self):
        return Expression(-self.vexity,
                          -self.sign,
                          '-' + str(self), 
                          [self])
    
    # def __le__(self,other):
    #     if iscvx(self) and isccv(other):
    #         return LeqConstraint(self,other)
    #     else:
    #         raise Exception("Cannot have '%s <= %s'" % (self.vexity_names[self.vexity], other.vexity_names[self.vexity]))
    
    # def __ge__(self,other):
    #     if isccv(self) and iscvx(other):
    #         return GeqConstraint(self,other)
    #     else:
    #         raise Exception("Cannot have '%s >= %s'" % (self.vexity_names[self.vexity], other.vexity_names[self.vexity]))
    
    # def __eq__(self,other):
    #     if isaff(self) and isaff(other):
    #         return EqConstraint(self,other)
    #     else:
    #         raise Exception("Cannot have '%s == %s'" % (self.vexity_names[self.vexity], other.vexity_names[self.vexity]))
            
    def __lt__(self, other): return NotImplemented
    def __gt__(self, other): return NotImplemented
    def __ne__(self, other): return NotImplemented
    
    def __repr__(self):
        """Representation in Python"""
        return "Expression(%s, %s, %s, %s)" % (self.vexity, self.sign, self.name, self.subexpressions)
    
    def __str__(self):
        """String representation"""
        return self.name


class Variable(Expression):
    """ A convex optimization variable. """
    def __init__(self, name):
        super(Variable, self).__init__(Vexity(Vexity.AFFINE_KEY),
                                       Sign(Sign.UNKNOWN_KEY),
                                       name,
                                       [])
    
    def __repr__(self):
        return "Variable(%s)" % (self.name)

    def __str__(self):
        return self.name
        
class Parameter(Expression):
    """ A convex optimization parameter. """
    def __init__(self, name, sign):
        super(Parameter, self).__init__(Vexity(Vexity.CONSTANT_KEY),
                                       sign,
                                       name,
                                       [])        
    def __repr__(self):
        return "Parameter(%s, %s)" % (self.name, self.sign)
            
    def __str__(self):
        return self.name
    
        
# class Constant(Expression):
#     # value = 0.0
    
#     def __init__(self, value):
#         if value >= 0:
#             sign = POSITIVE
#         else:
#             sign = NEGATIVE
#         super(Constant, self).__init__(AFFINE, sign, Scalar(), str(value), LinearFunc.constant(value))
        
#     def __repr__(self):
#         return "Constant(%s)" % self.name
    
#     def scoop(self):
#         """Declaration of variable in SCOOP lang"""
#         return "variable %s %s" % ( str(self.name), str.lower(str(self.shape)) )