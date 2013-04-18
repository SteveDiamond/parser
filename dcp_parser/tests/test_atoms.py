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
        self.const_exp = Expression(Curvature.CONSTANT, Sign.UNKNOWN, 'const_exp')
        self.aff_exp = Expression(Curvature.AFFINE, Sign.UNKNOWN, 'aff_exp')
        self.cvx_exp = Expression(Curvature.CONVEX, Sign.UNKNOWN, 'convex_exp')
        self.conc_exp = Expression(Curvature.CONCAVE, Sign.UNKNOWN, 'conc_exp')
        self.noncvx_exp = Expression(Curvature.NONCONVEX, Sign.UNKNOWN, 'noncvx_exp')

        self.cvx_pos = Expression(Curvature.CONVEX, Sign.POSITIVE, 'cvx_pos')
        self.cvx_neg = Expression(Curvature.CONVEX, Sign.NEGATIVE, 'cvx_neg')
        self.conc_pos = Expression(Curvature.CONCAVE, Sign.POSITIVE, 'conc_pos')
        self.conc_neg = Expression(Curvature.CONCAVE, Sign.NEGATIVE, 'conc_neg')

        self.increasing = Monotonicity.INCREASING
        self.decreasing = Monotonicity.DECREASING
        self.nonmonotonic = Monotonicity.NONMONOTONIC

    # Test application of DCP composition rules to determine curvature.
    def test_dcp_curvature(self):
        monotonicities = [self.increasing, self.decreasing]
        args = [self.cvx_exp, self.conc_exp]
        assert_equals(Atom.dcp_curvature(Curvature.CONVEX, args, monotonicities), Curvature.CONVEX)

        args = [self.conc_exp, self.aff_exp]
        assert_equals(Atom.dcp_curvature(Curvature.CONCAVE, args, monotonicities), Curvature.CONCAVE)
        assert_equals(Atom.dcp_curvature(Curvature.AFFINE, args, monotonicities), Curvature.CONCAVE)
        assert_equals(Atom.dcp_curvature(Curvature.NONCONVEX, args, monotonicities), Curvature.NONCONVEX)

        args = [self.const_exp, self.const_exp]
        assert_equals(Atom.dcp_curvature(Curvature.NONCONVEX, args, monotonicities), Curvature.CONSTANT)

        monotonicities = [self.nonmonotonic, self.increasing, self.decreasing]
        args = [self.const_exp, self.cvx_exp, self.aff_exp]
        assert_equals(Atom.dcp_curvature(Curvature.CONVEX, args, monotonicities), Curvature.CONVEX)
        assert_equals(Atom.dcp_curvature(Curvature.CONCAVE, args, monotonicities), Curvature.NONCONVEX)

        args = [self.aff_exp, self.aff_exp, self.cvx_exp]
        assert_equals(Atom.dcp_curvature(Curvature.CONCAVE, args, monotonicities), Curvature.CONCAVE)

        args = [self.cvx_exp, self.aff_exp, self.aff_exp]
        assert_equals(Atom.dcp_curvature(Curvature.CONCAVE, args, monotonicities), Curvature.NONCONVEX)

    # Test specific atoms.
    def test_square(self):
        assert_equals(Square(self.cvx_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Square(self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Square(self.cvx_pos).curvature(), Curvature.CONVEX)

    def test_log_sum_exp(self):
        assert_equals(Log_sum_exp(self.cvx_exp, self.cvx_exp).curvature(), Curvature.CONVEX)
        assert_equals(Log_sum_exp(self.cvx_exp, self.aff_exp).curvature(), Curvature.CONVEX)
        assert_equals(Log_sum_exp(self.conc_exp, self.cvx_exp).curvature(), Curvature.NONCONVEX)
        # Check error message
        try:
            Log_sum_exp()
            assert False
        except Exception, e:
            assert_equals(str(e), 'No arguments given to log_sum_exp.')

    def test_max(self):
        assert_equals(Max(self.cvx_pos, self.cvx_neg).sign(), Sign.POSITIVE)
        assert_equals(Max(self.cvx_pos, self.cvx_neg).curvature(), Curvature.CONVEX)

        assert_equals(Max(Constant(0), self.cvx_neg).sign(), Sign.ZERO)
        assert_equals(Max(self.conc_exp).curvature(), Curvature.NONCONVEX)

        assert_equals(Max(Variable('a'), Constant(2)).sign(), Sign.POSITIVE)

    def test_log(self):
        assert_equals(Log(self.conc_exp).curvature(), Curvature.CONCAVE)
        assert_equals(Log(self.cvx_exp).curvature(), Curvature.NONCONVEX)
        # Check error message
        try:
            Log(Constant(-2))
            assert False
        except Exception, e:
            assert_equals(str(e), 'log only accepts positive arguments.')

    def test_min(self):
        assert_equals(Min(self.conc_pos, self.conc_neg).sign(), Sign.NEGATIVE)
        assert_equals(Min(self.conc_pos, self.conc_neg).curvature(), Curvature.CONCAVE)

        assert_equals(Min(Constant(0), self.conc_pos).sign(), Sign.ZERO)
        assert_equals(Min(self.cvx_exp).curvature(), Curvature.NONCONVEX)

        assert_equals(Min(Variable('a'), Constant(-2)).sign(), Sign.NEGATIVE)

    def test_sum(self):
        assert_equals(Sum(Constant(2), Constant(0)).sign(), Sign.POSITIVE)
        assert_equals(Sum(self.cvx_exp, self.cvx_exp, self.aff_exp).curvature(), Curvature.CONVEX)
        assert_equals(Sum(self.conc_exp, self.cvx_exp, self.aff_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum(Constant(2), Constant(0), self.aff_exp).curvature(), Curvature.AFFINE)

    def test_geo_mean(self):
        assert_equals(Geo_mean(self.conc_exp, self.aff_exp, Constant(2)).curvature(), Curvature.CONCAVE)
        assert_equals(Geo_mean(self.conc_exp, self.aff_exp, Constant(2)).sign(), Sign.POSITIVE)
        assert_equals(Geo_mean(self.conc_exp, self.aff_exp, self.cvx_exp).curvature(), Curvature.NONCONVEX)
        assert_raises(Exception, Geo_mean, Constant(-2))
        # Check error message
        try:
            Geo_mean(Constant(-2))
            assert False
        except Exception, e:
            assert_equals(str(e), 'geo_mean does not accept negative arguments.')

    def test_sqrt(self):
        assert_equals(Sqrt(self.conc_exp).curvature(), Curvature.CONCAVE)
        assert_equals(Sqrt(self.aff_exp).sign(), Sign.POSITIVE)
        assert_equals(Sqrt(self.cvx_exp).curvature(), Curvature.NONCONVEX)
        assert_raises(Exception, Sqrt, Constant(-2))

    def test_log_normcdf(self):
        assert_equals(Log_normcdf(self.conc_exp).curvature(), Curvature.CONCAVE)
        assert_equals(Log_normcdf(self.cvx_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Log_normcdf(self.cvx_exp).sign(), Sign.UNKNOWN)

    def test_exp(self):
        assert_equals(Exp(self.cvx_exp).curvature(), Curvature.CONVEX)
        assert_equals(Exp(self.conc_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Exp(self.cvx_exp).sign(), Sign.POSITIVE)

    def test_norm(self):
        assert_equals(Norm(self.cvx_pos, self.aff_exp, self.const_exp, 1341.143).curvature(), Curvature.CONVEX)
        assert_equals(Norm(self.cvx_pos, self.aff_exp, self.const_exp, 2).sign(), Sign.POSITIVE)

        assert_equals(Norm(self.conc_neg, 'Inf').curvature(), Curvature.CONVEX)
        assert_equals(Norm(self.cvx_neg, 'Inf').curvature(), Curvature.NONCONVEX)

        # Check error message
        try:
            Norm(Constant(-2), 0)
            assert False
        except Exception, e:
            assert_equals(str(e), 'Invalid p-norm, p = 0')

        # Check error message
        try:
            Norm(Constant(-2), 'not inf')
            assert False
        except Exception, e:
            assert_equals(str(e), 'Invalid p-norm, p = not inf')

    def test_abs(self):
        assert_equals(Abs(self.aff_exp).curvature(), Curvature.CONVEX)
        assert_equals(Abs(self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Abs(self.cvx_neg).curvature(), Curvature.NONCONVEX)
        assert_equals(Abs(self.noncvx_exp).sign(), Sign.POSITIVE)

    def test_berhu(self):
        assert_equals(Berhu(self.aff_exp).curvature(), Curvature.CONVEX)
        assert_equals(Berhu(self.conc_neg,3).curvature(), Curvature.CONVEX)
        assert_equals(Berhu(self.cvx_neg,2).curvature(), Curvature.NONCONVEX)
        assert_equals(Berhu(self.noncvx_exp).sign(), Sign.POSITIVE)

        # Check error message
        try:
            Berhu(Constant(-2), 0)
            assert False
        except Exception, e:
            assert_equals(str(e), 'Invalid M for berhu function, M = 0')

    def test_entr(self):
        assert_equals(Entr(self.aff_exp).curvature(), Curvature.CONCAVE)
        assert_equals(Entr(self.conc_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Entr(self.cvx_exp).sign(), Sign.UNKNOWN)

    def test_huber(self):
        assert_equals(Huber(self.aff_exp).curvature(), Curvature.CONVEX)
        assert_equals(Huber(self.conc_neg,3).curvature(), Curvature.CONVEX)
        assert_equals(Huber(self.cvx_neg,2).curvature(), Curvature.NONCONVEX)
        assert_equals(Huber(self.noncvx_exp).sign(), Sign.POSITIVE)

        # Check error message
        try:
            Huber(Constant(-2), 0)
            assert False
        except Exception, e:
            assert_equals(str(e), 'Invalid M for huber function, M = 0')

    def test_huber_pos(self):
        assert_equals(Huber_pos(self.aff_exp).curvature(), Curvature.CONVEX)
        assert_equals(Huber_pos(self.conc_neg,3).curvature(), Curvature.CONSTANT)
        assert_equals(Huber_pos(self.cvx_exp,2).curvature(), Curvature.CONVEX)
        assert_equals(Huber_pos(self.noncvx_exp).sign(), Sign.POSITIVE)

        # Check error message
        try:
            Huber_pos(Constant(-2), 0)
            assert False
        except Exception, e:
            assert_equals(str(e), 'Invalid M for huber_pos function, M = 0')

    def test_huber_circ(self):
        assert_equals(Huber_circ(self.aff_exp, self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Huber_circ(self.conc_neg, self.cvx_neg, 3).curvature(), Curvature.NONCONVEX)
        assert_equals(Huber_circ(self.aff_exp, self.cvx_pos, 2).curvature(), Curvature.CONVEX)
        assert_equals(Huber_circ(self.noncvx_exp).sign(), Sign.POSITIVE)

        # Check error message
        try:
            Huber_circ(Constant(-2), 0)
            assert False
        except Exception, e:
            assert_equals(str(e), 'Invalid M for huber_circ function, M = 0')

    def test_inv_pos(self):
        assert_equals(Inv_pos(self.cvx_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Inv_pos(self.conc_exp).curvature(), Curvature.CONVEX)
        # Check error message
        try:
            Inv_pos(Constant(-2))
            assert False
        except Exception, e:
            assert_equals(str(e), 'inv_pos only accepts positive arguments.')

    def test_kl_div(self):
        assert_equals(Kl_div(self.aff_exp, self.aff_exp).curvature(), Curvature.CONVEX)
        assert_equals(Kl_div(self.conc_exp, self.const_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Kl_div(self.cvx_exp, self.noncvx_exp).sign(), Sign.UNKNOWN)

        # Check error message
        try:
            Kl_div(Constant(-2), Constant(-1))
            assert False
        except Exception, e:
            assert_equals(str(e), 'kl_div does not accept negative arguments.')

         # Check error message
        try:
            Kl_div(Constant(0), Constant(1))
            assert False
        except Exception, e:
            assert_equals(str(e), 'kl_div(x,y) requires that x == 0 if and only if y == 0.',)

    def test_norm_largest(self):
        assert_equals(Norm_largest(self.cvx_pos, self.aff_exp, self.conc_neg, 2).curvature(), Curvature.CONVEX)
        assert_equals(Norm_largest(self.cvx_pos, self.aff_exp, self.const_exp, 2).sign(), Sign.POSITIVE)

        assert_equals(Norm_largest(self.conc_pos, 1).curvature(), Curvature.NONCONVEX)

        # Check error message
        try:
            Norm_largest(Constant(-2), 'invalid')
            assert False
        except Exception, e:
            assert_equals(str(e), "Invalid value for k in norm_largest(*vector,k).")

    def test_pos(self):
        assert_equals(Pos(self.conc_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Pos(self.conc_neg).curvature(), Curvature.CONSTANT)
        assert_equals(Pos(self.cvx_exp).curvature(), Curvature.CONVEX)
        assert_equals(Pos(self.cvx_pos).sign(), Sign.POSITIVE)

    def test_pow_p(self):
        assert_equals(Pow_p(self.cvx_pos,-1).curvature(), Curvature.NONCONVEX)
        assert_equals(Pow_p(self.conc_neg,-1).curvature(), Curvature.CONVEX)
        assert_equals(Pow_p(self.cvx_pos,-1).sign(), Sign.POSITIVE)

        assert_equals(Pow_p(self.cvx_pos,0.5).curvature(), Curvature.NONCONVEX)
        assert_equals(Pow_p(self.cvx_pos,0.5).sign(), Sign.POSITIVE)
        assert_equals(Pow_p(self.noncvx_exp, 0.5).sign(), Sign.UNKNOWN)
        assert_equals(Pow_p(self.conc_neg,0.5).curvature(), Curvature.CONCAVE)
        assert_equals(Pow_p(self.conc_neg,0.5).sign(), Sign.NEGATIVE)

        assert_equals(Pow_p(self.cvx_pos,2).curvature(), Curvature.CONVEX)
        assert_equals(Pow_p(self.conc_neg,2).curvature(), Curvature.CONVEX)
        assert_equals(Pow_p(self.cvx_neg,2).curvature(), Curvature.NONCONVEX)
        assert_equals(Pow_p(self.conc_pos,2).curvature(), Curvature.NONCONVEX)
        assert_equals(Pow_p(self.noncvx_exp, 2).sign(), Sign.POSITIVE)

        # Check error message
        try:
            Pow_p(Constant(-2), 'wrong')
            assert False
        except Exception, e:
            assert_equals(str(e), 'Invalid p for pow_p(x,p), p = wrong.')

    def test_pow_abs(self):
        assert_equals(Pow_abs(self.cvx_pos,2).curvature(), Curvature.CONVEX)
        assert_equals(Pow_abs(self.conc_neg,2).curvature(), Curvature.CONVEX)
        assert_equals(Pow_abs(self.cvx_neg,2).curvature(), Curvature.NONCONVEX)
        assert_equals(Pow_abs(self.conc_pos,2).curvature(), Curvature.NONCONVEX)
        assert_equals(Pow_abs(self.noncvx_exp, 2).sign(), Sign.POSITIVE)

        # Check error message
        try:
            Pow_abs(Constant(-2), 0)
            assert False
        except Exception, e:
            assert_equals(str(e), 'Must have p >= 1 for pow_abs(x,p), but have p = 0.')
        
    def test_pow_pos(self):
        assert_equals(Pow_pos(self.cvx_pos,2).curvature(), Curvature.CONVEX)
        assert_equals(Pow_pos(self.conc_neg,2).curvature(), Curvature.CONSTANT)
        assert_equals(Pow_pos(self.conc_pos,2).curvature(), Curvature.NONCONVEX)
        assert_equals(Pow_pos(self.noncvx_exp, 2).sign(), Sign.POSITIVE)

        # Check error message
        try:
            Pow_pos(Constant(-2), 0)
            assert False
        except Exception, e:
            assert_equals(str(e), 'Must have p >= 1 for pow_pos(x,p), but have p = 0.')

    def test_square_abs(self):
        assert_equals(Square_abs(self.cvx_pos).curvature(), Curvature.CONVEX)
        assert_equals(Square_abs(self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Square_abs(self.conc_pos).curvature(), Curvature.NONCONVEX)
        assert_equals(Square_abs(self.noncvx_exp).sign(), Sign.POSITIVE)

    def test_square_pos(self):
        assert_equals(Square_pos(self.cvx_exp).curvature(), Curvature.CONVEX)
        assert_equals(Square_pos(self.conc_neg).curvature(), Curvature.CONSTANT)
        assert_equals(Square_pos(self.conc_pos).curvature(), Curvature.NONCONVEX)
        assert_equals(Square_pos(self.noncvx_exp).sign(), Sign.POSITIVE)
        
    def test_rel_entr(self):
        assert_equals(Rel_entr(self.aff_exp, self.const_exp).curvature(), Curvature.CONVEX)
        assert_equals(Rel_entr(self.conc_exp, self.aff_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Rel_entr(self.cvx_exp, self.noncvx_exp).sign(), Sign.UNKNOWN)

    def test_quad_over_lin(self):
        assert_equals(Quad_over_lin(self.cvx_pos, self.conc_exp).curvature(), Curvature.CONVEX)
        assert_equals(Quad_over_lin(self.cvx_pos, self.aff_exp, self.conc_neg, self.conc_exp).curvature(), 
            Curvature.CONVEX)
        assert_equals(Quad_over_lin(self.conc_neg, self.cvx_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Quad_over_lin(self.cvx_exp, self.cvx_pos, self.conc_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Quad_over_lin(self.noncvx_exp, self.cvx_pos, self.conc_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Quad_over_lin(self.noncvx_exp, self.cvx_pos, self.conc_exp).sign(), Sign.POSITIVE)

        # Check error message
        try:
            Quad_over_lin(self.cvx_pos)
            assert False
        except Exception, e:
            assert_equals(str(e), 'quad_over_lin called with too few arguments.')

        # Check error message
        try:
            Quad_over_lin(self.cvx_pos, self.cvx_neg)
            assert False
        except Exception, e:
            assert_equals(str(e), 'quad_over_lin only accepts positive divisor arguments.')

    def test_sum_square(self):
        assert_equals(Sum_square(self.cvx_pos, self.aff_exp, self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Sum_square(self.cvx_neg, self.aff_exp, self.conc_neg).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square(self.conc_neg, self.cvx_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square(self.cvx_neg, self.conc_neg).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square(self.noncvx_exp, self.cvx_pos).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square(self.noncvx_exp, self.cvx_pos).sign(), Sign.POSITIVE)

    def test_sum_square_abs(self):
        assert_equals(Sum_square_abs(self.cvx_pos, self.aff_exp, self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Sum_square_abs(self.cvx_neg, self.aff_exp, self.conc_neg).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square_abs(self.conc_neg, self.cvx_neg).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square_abs(self.noncvx_exp, self.cvx_pos).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square_abs(self.noncvx_exp, self.cvx_pos).sign(), Sign.POSITIVE)

    def test_sum_square_pos(self):
        assert_equals(Sum_square_pos(self.cvx_pos, self.aff_exp, self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Sum_square_pos(self.cvx_neg, self.aff_exp, self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Sum_square_pos(self.conc_neg, self.cvx_neg).curvature(), Curvature.CONSTANT)
        assert_equals(Sum_square_pos(self.conc_neg, self.cvx_neg).sign(), Sign.ZERO)
        assert_equals(Sum_square_pos(self.noncvx_exp, self.cvx_pos).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square_pos(self.noncvx_exp, self.cvx_pos).sign(), Sign.POSITIVE)

    def test_sum_largest(self):
        assert_equals(Sum_largest(self.cvx_pos, self.aff_exp, 2).curvature(), Curvature.CONVEX)
        assert_equals(Sum_largest(self.cvx_pos, self.aff_exp, 2).sign(), Sign.UNKNOWN)

        assert_equals(Sum_largest(self.conc_exp, 1).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_smallest(self.cvx_exp, self.noncvx_exp, 1).curvature(), Curvature.NONCONVEX)
        # Check error message
        try:
            Sum_largest(self.cvx_pos, 'invalid')
            assert False
        except Exception, e:
            assert_equals(str(e), "Invalid value for k in sum_largest(*vector,k).")

    def test_sum_smallest(self):
        assert_equals(Sum_smallest(self.cvx_exp, self.aff_exp, 2).curvature(), Curvature.CONCAVE)
        assert_equals(Sum_smallest(self.cvx_exp, self.aff_exp, 2).sign(), Sign.UNKNOWN)

        assert_equals(Sum_smallest(self.conc_exp, 1).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_smallest(self.conc_exp, self.noncvx_exp, 1).curvature(), Curvature.NONCONVEX)
        # Check error message
        try:
            Sum_smallest(self.cvx_pos, 'invalid')
            assert False
        except Exception, e:
            assert_equals(str(e), "Invalid value for k in sum_smallest(*vector,k).")