from dcp_parser.expression.curvature import Curvature
from dcp_parser.expression.sign import Sign
from dcp_parser.expression.expression import *
from dcp_parser.atomic.monotonicity import Monotonicity
from dcp_parser.atomic.atoms import *
from nose.tools import *

class TestAtoms(object):
    """ Unit tests for the atomic/monotonicity class. """
    @classmethod
    def setup_class(self):
        self.unknown = Sign.UNKNOWN

        self.constant = Curvature.CONSTANT
        self.affine = Curvature.AFFINE
        self.convex = Curvature.CONVEX
        self.concave = Curvature.CONCAVE
        self.nonconvex = Curvature.NONCONVEX

        self.const_exp = Expression(self.constant, self.unknown, 'const_exp')
        self.aff_exp = Expression(self.affine, self.unknown, 'aff_exp')
        self.cvx_exp = Expression(self.convex, self.unknown, 'convex_exp')
        self.conc_exp = Expression(self.concave, self.unknown, 'conc_exp')
        self.noncvx_exp = Expression(self.nonconvex, self.unknown, 'noncvx_exp')

        self.increasing = Monotonicity.INCREASING
        self.decreasing = Monotonicity.DECREASING
        self.nonmonotonic = Monotonicity.NONMONOTONIC

    # Test application of DCP composition rules to determine curvature.
    def test_dcp_curvature(self):
        monotonicities = [self.increasing, self.decreasing]
        args = [self.cvx_exp, self.conc_exp]
        assert_equals(Atom.dcp_curvature(self.convex, args, monotonicities), self.convex)

        args = [self.conc_exp, self.aff_exp]
        assert_equals(Atom.dcp_curvature(self.concave, args, monotonicities), self.concave)
        assert_equals(Atom.dcp_curvature(self.affine, args, monotonicities), self.concave)
        assert_equals(Atom.dcp_curvature(self.nonconvex, args, monotonicities), self.nonconvex)

        args = [self.const_exp, self.const_exp]
        assert_equals(Atom.dcp_curvature(self.nonconvex, args, monotonicities), self.constant)

        monotonicities = [self.nonmonotonic, self.increasing, self.decreasing]
        args = [self.const_exp, self.cvx_exp, self.aff_exp]
        assert_equals(Atom.dcp_curvature(self.convex, args, monotonicities), self.convex)
        assert_equals(Atom.dcp_curvature(self.concave, args, monotonicities), self.nonconvex)

        args = [self.aff_exp, self.aff_exp, self.cvx_exp]
        assert_equals(Atom.dcp_curvature(self.concave, args, monotonicities), self.concave)

        args = [self.cvx_exp, self.aff_exp, self.aff_exp]
        assert_equals(Atom.dcp_curvature(self.concave, args, monotonicities), self.nonconvex)

    # Test specific atoms.
    def test_square(self):
        assert_equals(Square(self.cvx_exp).curvature(), self.nonconvex)
        exp = Expression(self.concave, Sign.NEGATIVE, 'exp')
        assert_equals(Square(exp).curvature(), self.convex)

    def test_log_sum_exp(self):
        assert_equals(Log_sum_exp(self.cvx_exp, self.cvx_exp).curvature(), self.convex)
        assert_equals(Log_sum_exp(self.cvx_exp, self.aff_exp).curvature(), self.convex)
        assert_equals(Log_sum_exp(self.conc_exp, self.cvx_exp).curvature(), self.nonconvex)

    def test_max(self):
        cvx_pos = Expression(Curvature.CONVEX, Sign.POSITIVE, 'cvx_pos')
        cvx_neg = Expression(Curvature.CONVEX, Sign.NEGATIVE, 'cvx_pos')
        assert_equals(Max(cvx_pos, cvx_neg).sign(), Sign.POSITIVE)
        assert_equals(Max(cvx_pos, cvx_neg).curvature(), Curvature.CONVEX)

        assert_equals(Max(Constant(0), cvx_neg).sign(), Sign.ZERO)
        assert_equals(Max(self.conc_exp).curvature(), Curvature.NONCONVEX)

    def test_log(self):
        assert_equals(Log(self.conc_exp).curvature(), Curvature.CONCAVE)
        assert_raises(Exception, Log, Constant(-2))