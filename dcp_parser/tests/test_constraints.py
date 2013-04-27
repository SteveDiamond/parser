from dcp_parser.expression.curvature import Curvature
from dcp_parser.expression.sign import Sign
from dcp_parser.expression.expression import *
from dcp_parser.expression.constraints import *
from nose.tools import *

class TestConstraints(object):
    """ Unit tests for the expression/constraints module. """
    @classmethod
    def setup_class(self):
        self.const_exp = Expression(Curvature.CONSTANT, Sign.UNKNOWN, 'const_exp')
        self.aff_exp = Expression(Curvature.AFFINE, Sign.UNKNOWN, 'aff_exp')
        self.cvx_exp = Expression(Curvature.CONVEX, Sign.UNKNOWN, 'convex_exp')
        self.conc_exp = Expression(Curvature.CONCAVE, Sign.UNKNOWN, 'conc_exp')
        self.noncvx_exp = Expression(Curvature.NONCONVEX, Sign.UNKNOWN, 'noncvx_exp')

        self.dcp_violation = "Disciplined convex programming violation:\n"

    # Test the equality constraint class.
    # Also tests error messages.
    def test_eq_constraint(self):
        eq_valid = EqConstraint(self.const_exp, self.aff_exp)
        assert_equals(len(eq_valid.errors), 0)

        eq_valid = EqConstraint(self.aff_exp, self.aff_exp)
        assert_equals(len(eq_valid.errors), 0)

        eq_invalid = EqConstraint(self.cvx_exp, self.aff_exp)
        assert_equals(len(eq_invalid.errors), 1)
        base_msg = "Illegal constraint: convex == affine"
        assert_equals(str(eq_invalid.errors[0]), self.dcp_violation + base_msg)

        eq_invalid = EqConstraint(self.const_exp, self.conc_exp)
        assert_equals(len(eq_invalid.errors), 1)
        base_msg = "Illegal constraint: constant == concave"
        assert_equals(str(eq_invalid.errors[0]), self.dcp_violation + base_msg)

        eq_invalid = EqConstraint(self.noncvx_exp, self.conc_exp)
        assert_equals(len(eq_invalid.errors), 1)
        base_msg = "Illegal constraint: non-convex == concave"
        assert_equals(str(eq_invalid.errors[0]), self.dcp_violation + base_msg)

    # Test the <= constraint class.
    # Also tests error messages.
    def test_leq_constraint(self):
        leq_valid = LeqConstraint(self.const_exp, self.aff_exp)
        assert_equals(len(leq_valid.errors), 0)

        leq_valid = LeqConstraint(self.cvx_exp, self.aff_exp)
        assert_equals(len(leq_valid.errors), 0)

        leq_valid = LeqConstraint(self.cvx_exp, self.conc_exp)
        assert_equals(len(leq_valid.errors), 0)

        leq_invalid = LeqConstraint(self.const_exp, self.cvx_exp)
        assert_equals(len(leq_invalid.errors), 1)
        base_msg = "Illegal constraint: constant <= convex"
        assert_equals(str(leq_invalid.errors[0]), self.dcp_violation + base_msg)

        leq_invalid = LeqConstraint(self.conc_exp, self.aff_exp)
        assert_equals(len(leq_invalid.errors), 1)
        base_msg = "Illegal constraint: concave <= affine"
        assert_equals(str(leq_invalid.errors[0]), self.dcp_violation + base_msg)

        leq_invalid = LeqConstraint(self.cvx_exp, self.noncvx_exp)
        assert_equals(len(leq_invalid.errors), 1)
        base_msg = "Illegal constraint: convex <= non-convex"
        assert_equals(str(leq_invalid.errors[0]), self.dcp_violation + base_msg)

    # Test the >= constraint class.
    # Also tests error messages.
    def test_geq_constraint(self):
        geq_valid = GeqConstraint(self.const_exp, self.aff_exp)
        assert_equals(len(geq_valid.errors), 0)

        geq_valid = GeqConstraint(self.conc_exp, self.aff_exp)
        assert_equals(len(geq_valid.errors), 0)

        geq_valid = GeqConstraint(self.conc_exp, self.cvx_exp)
        assert_equals(len(geq_valid.errors), 0)

        geq_invalid = GeqConstraint(self.cvx_exp, self.const_exp)
        assert_equals(len(geq_invalid.errors), 1)
        base_msg = "Illegal constraint: convex >= constant"
        assert_equals(str(geq_invalid.errors[0]), self.dcp_violation + base_msg)

        geq_invalid = GeqConstraint(self.aff_exp, self.conc_exp)
        assert_equals(len(geq_invalid.errors), 1)
        base_msg = "Illegal constraint: affine >= concave"
        assert_equals(str(geq_invalid.errors[0]), self.dcp_violation + base_msg)

        geq_invalid = GeqConstraint(self.cvx_exp, self.noncvx_exp)
        assert_equals(len(geq_invalid.errors), 1)
        base_msg = "Illegal constraint: convex >= non-convex"
        assert_equals(str(geq_invalid.errors[0]), self.dcp_violation + base_msg)

    # Test short_name
    def test_short_name(self):
        leq = LeqConstraint(self.const_exp, self.aff_exp)
        assert_equals(leq.short_name, "<=")

        geq = GeqConstraint(self.const_exp, self.aff_exp)
        assert_equals(geq.short_name, ">=")

        eq = EqConstraint(self.const_exp, self.aff_exp)
        assert_equals(eq.short_name, "==")