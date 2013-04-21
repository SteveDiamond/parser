import settings
from dcp_violation import DCPViolation

class ConstraintError(DCPViolation):
    """ Represents a DCP violation through an improper constraint."""
    BASE_MSG = "Illegal constraint:"

    def __init__(self, constraint_str, lh_curvature, rh_curvature):
        self.constraint_str = constraint_str
        self.lh_curvature = lh_curvature
        self.rh_curvature = rh_curvature

    def __str__(self):
        error_str = " ".join([ConstraintError.BASE_MSG, 
                              ConstraintError.type_to_name(self.lh_curvature),
                              self.constraint_str,
                              ConstraintError.type_to_name(self.rh_curvature)])
        return settings.DCP_ERROR_MSG + error_str