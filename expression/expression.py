from utils import error_msg, id_wrapper, \
    isunknown, ispositive, isnegative, \
    isaff, iscvx, isccv, ismatrix, isscalar, isvector
    
from sign import POSITIVE, NEGATIVE, UNKNOWN
from constraint import EqConstraint, LeqConstraint, GeqConstraint

# the ordering here matters. we use a bitwise OR to accomplish vexity
# inference. 
#   AFFINE (0) | ANYTHING = ANYTHING
#   CONVEX (1) | CONCAVE (2) = NONCONVEX (3)
#   SAME | SAME = SAME

# should i make these classes so i can print them?
AFFINE,CONVEX,CONCAVE,NONCONVEX = range(4)
        
# Expression evaluator goes here....
class Expression(object):
    """
    A convex optimization expression.
    Records sign, vexity, string representation, and component expressions.
    """
    
    vexity_lookup = {'AFFINE': AFFINE, 'CONVEX': CONVEX, 'CONCAVE': CONCAVE, 'NONCONVEX': NONCONVEX}
    vexity_names = ['AFFINE', 'CONVEX', 'CONCAVE', 'NONCONVEX']
    
    negate = {AFFINE: AFFINE, CONVEX: CONCAVE, CONCAVE: CONVEX, NONCONVEX: NONCONVEX}
    
    def __init__(self, vexity, sign, name, func):
        self.vexity = vexity
        self.sign = sign
        self.shape = shape
        self.name = name
        if func: self.linfunc = func
        else: self.linfunc = LinearFunc.variable(name)
        
    def value(self):
        return self.linfunc.constant_value()
    
    def __add__(self, other):
        vexity = self.vexity | other.vexity
        sign = self.sign + other.sign
        shape = self.shape + other.shape
        linfunc = self.linfunc + other.linfunc
        name = str(linfunc)
        
        return Expression(vexity, sign, shape, name, linfunc)
    
    def __sub__(self, other):
        vexity = self.vexity | self.negate[other.vexity]
        sign = self.sign + (-other.sign)
        shape = self.shape + (-other.shape)
        linfunc = self.linfunc - other.linfunc
        name = str(linfunc)
        
        return Expression(vexity, sign, shape, name, linfunc)

    def __mul__(self, other):
        # expressions are always affine expressions
        vexity = AFFINE
        # "other" is always affine (this is just a sanity check)
        if self.vexity is not AFFINE:
            raise Exception("Cannot multiply with non-affine on left.")
            
        if ispositive(self): 
            vexity |= other.vexity
        elif isnegative(self):
            vexity |= self.negate[other.vexity]
        else:
            if other.vexity is not AFFINE:
                vexity = NONCONVEX

        sign = self.sign * other.sign
        shape = self.shape * other.shape
        linfunc = self.linfunc * other.linfunc
        name = str(linfunc)
        
        return Expression(vexity, sign, shape, name, linfunc)
        
    def __neg__(self):
        vexity = self.negate[self.vexity]
        sign = -self.sign
        shape = -self.shape
        linfunc = -self.linfunc
        name = str(self.linfunc)
        return Expression(vexity, sign, shape, name, linfunc)
    
    def __le__(self,other):
        if iscvx(self) and isccv(other):
            return LeqConstraint(self,other)
        else:
            raise Exception("Cannot have '%s <= %s'" % (self.vexity_names[self.vexity], other.vexity_names[self.vexity]))
    
    def __ge__(self,other):
        if isccv(self) and iscvx(other):
            return GeqConstraint(self,other)
        else:
            raise Exception("Cannot have '%s >= %s'" % (self.vexity_names[self.vexity], other.vexity_names[self.vexity]))
    
    def __eq__(self,other):
        if isaff(self) and isaff(other):
            return EqConstraint(self,other)
        else:
            raise Exception("Cannot have '%s == %s'" % (self.vexity_names[self.vexity], other.vexity_names[self.vexity]))
            
    def __lt__(self, other): return NotImplemented
    def __gt__(self, other): return NotImplemented
    def __ne__(self, other): return NotImplemented
    
    def __repr__(self):
        """Representation in Python"""
        return "Expression(%s, %s, %s, %s, %s)" % (self.vexity, self.sign, self.shape, self.name, self.linfunc)
    
    def __str__(self):
        """String representation"""
        return self.name
    
    def scoop(self):
        """Declaration of expression in SCOOP lang"""
        return self.name


class Variable(Expression):
    def __init__(self, name, shape):
        if not ismatrix(shape):
            super(Variable, self).__init__(AFFINE, UNKNOWN, shape, name, LinearFunc.variable(name))
        else:
            raise TypeError("Cannot create a matrix variable.")
    
    def __repr__(self):
        return "Variable(%s, %s)" % (self.name, self.shape)
        
    def scoop(self):
        """Declaration of variable in SCOOP lang"""
        return "variable %s %s" % ( str(self.name), str.lower(str(self.shape)) )
        
class Parameter(Expression):
    def __init__(self, name, shape, sign):
        super(Parameter, self).__init__(AFFINE, sign, shape, name, LinearFunc.constant(name))
        
    def __repr__(self):
        return "Parameter(%s, %s, %s)" % (self.name, self.shape, self.sign)
            
    def __str__(self):
        return self.name
    
    def scoop(self):
        if isunknown(self):
            return "parameter %s %s" % ( str(self.name), str.lower(str(self.shape)) )
        else:
            return "parameter %s %s %s" % ( str(self.name), str.lower(str(self.shape)), str.lower(str(self.sign)) )
    
        
class Constant(Expression):
    # value = 0.0
    
    def __init__(self, value):
        if value >= 0:
            sign = POSITIVE
        else:
            sign = NEGATIVE
        super(Constant, self).__init__(AFFINE, sign, Scalar(), str(value), LinearFunc.constant(value))
        
    def __repr__(self):
        return "Constant(%s)" % self.name
    
    def scoop(self):
        """Declaration of variable in SCOOP lang"""
        return "variable %s %s" % ( str(self.name), str.lower(str(self.shape)) )

    
# convex, concave, affine decorators
# def convex(fn,*args):
#     def wrap(*args):
#         e = fn(*args)
#         e.vexity |= CONVEX
#         return e
#     return wrap
# 
# def concave(fn,*args):
#     def wrap(*args):
#         e = fn(*args)
#         e.vexity |= CONCAVE
#         return e.vexity
#     return wrap
# 
# def affine(fn,*args):
#     def wrap(*args):
#         e = fn(*args)
#         e.vexity |= AFFINE
#         return e
#     return wrap



# def expand_all_args(fn, *args):
#     """Ensures all args are variables"""
#     def wrap(*args):
#         evaluator = args[0]
#         expanded_args = map (evaluator.expand, args[1:])
#         e = fn(evaluator, *expanded_args)
#         return e
#     return wrap

    
# def fold_with(f):
#     """To help with constant folding"""
#     def wrapper(fn, *args):
#         def wrap(*args):
#             if (all(isinstance(e, Constant) for e in args[1:])):
#                 arg_vals = map (lambda e: e.value, args[1:])
#                 e = Constant( f(*arg_vals) )
#             else:
#                 e = fn(*args)
#             return e
#         return wrap
#     return wrapper

# globals...
# INCREASING, DECREASING, NONMONOTONE = range(3)

        
    