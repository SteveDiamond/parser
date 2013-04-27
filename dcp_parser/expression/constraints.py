import abc
from curvature import Curvature
from statement import Statement
from dcp_parser.error_messages.dcp_violation_factory import DCPViolationFactory

class Constraint(Statement):
    """ Abstract base class for all constraint types """
    __metaclass__ = abc.ABCMeta
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        errors = self.check_curvatures() 
        super(Constraint, self).__init__(self.CONSTRAINT_STR, [lhs,rhs], errors)

    # Returns errors if lhs and rhs curvatures are invalid.
    @abc.abstractmethod
    def check_curvatures(self):
        return NotImplemented

    def __repr__(self):
        """Representation in Python"""
        return "%s(%s, %s)" % (self.__class__.__name__,
                               self.rhs.__repr__(), 
                               self.lhs.__repr__())
    
    def __str__(self):
        """String representation"""
        return "%s %s %s" % (self.lhs, self.CONSTRAINT_STR, self.rhs)


class EqConstraint(Constraint):
    """ Represents an equality constraint """
    CONSTRAINT_STR = "=="

    # Checks whether lhs and rhs are both affine.
    # If not, returns an error.
    def check_curvatures(self):
        errors = []
        if not (self.lhs.curvature.is_affine() and self.rhs.curvature.is_affine()):
            errors = DCPViolationFactory.constraint_error(self.CONSTRAINT_STR, 
                                                          self.lhs.curvature, 
                                                          self.rhs.curvature)
        return errors

class LeqConstraint(Constraint):
    """ Represents a less than or equals constraint """
    CONSTRAINT_STR = "<="

    # Checks whether lhs is convex and rhs is concave.
    # If not, returns an error.
    def check_curvatures(self):
        errors = []
        if not (self.lhs.curvature.is_convex() and self.rhs.curvature.is_concave()):
            errors = DCPViolationFactory.constraint_error(self.CONSTRAINT_STR, 
                                                          self.lhs.curvature, 
                                                          self.rhs.curvature)
        return errors

class GeqConstraint(Constraint):
    """ Represents an greater than or equals constraint """
    CONSTRAINT_STR = ">="

    # Checks whether lhs is concave and rhs is convex.
    # If not, returns an error.
    def check_curvatures(self):
        errors = []
        if not (self.lhs.curvature.is_concave() and self.rhs.curvature.is_convex()):
            errors = DCPViolationFactory.constraint_error(self.CONSTRAINT_STR, 
                                                          self.lhs.curvature, 
                                                          self.rhs.curvature)
        return errors