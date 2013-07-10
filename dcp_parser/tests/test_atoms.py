from dcp_parser.expression.curvature import Curvature
from dcp_parser.expression.sign import Sign
from dcp_parser.expression.expression import *
from dcp_parser.atomic.monotonicity import Monotonicity
import dcp_parser.atomic.atom_loader as atom_loader
from dcp_parser.atomic.atoms import *
from nose.tools import *
import inspect

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

    # Test short names for atoms
    def test_short_names(self):
        atom_dict = atom_loader.generate_atom_dict()
        # Non-standard short names
        special_names = ['norm', 'norm_largest','huber','berhu','huber_pos','huber_circ','pow',
                         'pow_pos','pow_abs','sum_largest','sum_smallest'];
        
        # Test short names for all standard atoms
        for subclass in atom_loader.get_subclasses(Atom):
            name = subclass.__name__.lower()
            if name not in special_names:
                (args, varargs, keywords, defaults) = inspect.getargspec(subclass.__init__)
                new_args = [self.cvx_exp] * (len(args)-1)
                if varargs is not None:
                    new_args.append(self.cvx_exp)
                    new_args.append(self.cvx_exp)
                atom = subclass(*new_args)
                assert_equals(atom.short_name(), name)
        
        # Norm 
        exp = atom_dict['norm'](self.conc_exp, self.cvx_exp, 3)
        assert_equals(exp.short_name, 'norm(..., 3)')

        exp = atom_dict['norm'](self.conc_exp, self.cvx_exp, 'Inf')
        assert_equals(exp.short_name, 'norm(..., Inf)')

        # All Huber
        exp = atom_dict['huber'](self.conc_exp, 100)
        assert_equals(exp.short_name, 'huber(..., 100)')

        exp = atom_dict['berhu'](self.conc_exp, 100)
        assert_equals(exp.short_name, 'berhu(..., 100)')

        exp = atom_dict['huber_pos'](self.conc_exp, 100)
        assert_equals(exp.short_name, 'huber_pos(..., 100)')

        exp = atom_dict['huber_circ'](self.conc_exp, self.aff_exp, 100)
        assert_equals(exp.short_name, 'huber_circ(..., 100)')

        # All pow_p
        exp = atom_dict['pow'](self.cvx_exp, 0.5)
        assert_equals(exp.short_name, 'pow(..., 0.5)')

        exp = atom_dict['pow_pos'](self.cvx_exp, 1)
        assert_equals(exp.short_name, 'pow_pos(..., 1)')

        exp = atom_dict['pow_abs'](self.cvx_exp, 1)
        assert_equals(exp.short_name, 'pow_abs(..., 1)')

        # All sum_largest
        exp = atom_dict['sum_largest'](self.cvx_exp, self.noncvx_exp, self.aff_exp, 2.2)
        assert_equals(exp.short_name, 'sum_largest(..., 2.2)')

        exp = atom_dict['sum_smallest'](self.cvx_exp, self.noncvx_exp, self.aff_exp, 2.2)
        assert_equals(exp.short_name, 'sum_smallest(..., 2.2)')

    # Test specific atoms.
    def test_square(self):
        assert_equals(Square(self.cvx_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Square(self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Square(self.cvx_pos).curvature(), Curvature.CONVEX)
        # Test that the Atom has the proper subexpressions
        assert_equals(len(Square(self.cvx_pos).arguments()), 1)
        assert_not_equals(Square(self.cvx_pos).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_log_sum_exp(self):
        assert_equals(Log_sum_exp(self.cvx_exp, self.cvx_exp).curvature(), Curvature.CONVEX)
        assert_equals(Log_sum_exp(self.cvx_exp, self.aff_exp).curvature(), Curvature.CONVEX)
        assert_equals(Log_sum_exp(self.conc_exp, self.cvx_exp).curvature(), Curvature.NONCONVEX)

        # Check error message
        try:
            Log_sum_exp()
            assert False
        except Exception, e:
            assert_equals(str(e), "No arguments given to 'log_sum_exp'.")

        assert_equals(len(Log_sum_exp(self.conc_exp, self.cvx_exp).arguments()), 2)
        assert_not_equals(Log_sum_exp(self.conc_exp, self.cvx_exp).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_max(self):
        assert_equals(Max(self.cvx_pos, self.cvx_neg).sign(), Sign.POSITIVE)
        assert_equals(Max(self.cvx_pos, self.cvx_neg).curvature(), Curvature.CONVEX)

        assert_equals(Max(Constant(0)).sign(), Sign.POSITIVE)
        assert_equals(Max(Constant(0), self.cvx_neg).sign(), Sign.POSITIVE)
        assert_equals(Max(Constant(0), self.cvx_exp).sign(), Sign.POSITIVE)
        assert_equals(Max(Constant(0), self.cvx_exp, self.cvx_neg, self.cvx_pos).sign(), Sign.POSITIVE)
        assert_equals(Max(self.conc_exp).curvature(), Curvature.NONCONVEX)

        assert_equals(Max(Variable('a'), Constant(2)).sign(), Sign.POSITIVE)

        assert_equals(len(Max(self.cvx_pos, self.cvx_neg).arguments()), 2)
        assert_not_equals(Max(self.cvx_pos, self.cvx_neg).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_log(self):
        assert_equals(Log(self.conc_exp).curvature(), Curvature.CONCAVE)
        assert_equals(Log(self.cvx_exp).curvature(), Curvature.NONCONVEX)

        assert_equals(len(Log(self.cvx_exp).arguments()), 1)
        assert_not_equals(Log(self.cvx_exp).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_min(self):
        assert_equals(Min(self.conc_pos, self.conc_neg).sign(), Sign.NEGATIVE)
        assert_equals(Min(self.conc_pos, self.conc_neg).curvature(), Curvature.CONCAVE)

        assert_equals(Min(Constant(0)).sign(), Sign.NEGATIVE)
        assert_equals(Min(Constant(0), self.conc_pos).sign(), Sign.NEGATIVE)
        assert_equals(Min(Constant(0), self.conc_exp).sign(), Sign.NEGATIVE)
        assert_equals(Min(self.cvx_exp).curvature(), Curvature.NONCONVEX)

        assert_equals(Min(Variable('a'), Constant(-2)).sign(), Sign.NEGATIVE)

        assert_equals(len(Min(self.cvx_pos, self.cvx_neg).arguments()), 2)
        assert_not_equals(Min(self.cvx_pos, self.cvx_neg).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_sum(self):
        assert_equals(Sum(Constant(2), Constant(0)).sign(), Sign.POSITIVE)
        assert_equals(Sum(self.cvx_exp, self.cvx_exp, self.aff_exp).curvature(), Curvature.CONVEX)
        assert_equals(Sum(self.conc_exp, self.cvx_exp, self.aff_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum(Constant(2), Constant(0), self.aff_exp).curvature(), Curvature.AFFINE)

        assert_equals(len(Sum(self.cvx_pos, self.cvx_neg).arguments()), 2)
        assert_not_equals(Sum(self.cvx_pos, self.cvx_neg).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_geo_mean(self):
        assert_equals(Geo_mean(self.conc_exp, self.aff_exp, Constant(2)).curvature(), Curvature.CONCAVE)
        assert_equals(Geo_mean(self.conc_exp, self.aff_exp, Constant(2)).sign(), Sign.POSITIVE)
        assert_equals(Geo_mean(self.conc_exp, self.aff_exp, self.cvx_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Geo_mean(Constant(-2)).sign(), Sign.NEGATIVE)

        assert_equals(len(Geo_mean(self.cvx_pos, self.conc_pos).arguments()), 2)
        assert_not_equals(Geo_mean(self.cvx_pos, self.conc_pos).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_sqrt(self):
        assert_equals(Sqrt(self.conc_exp).curvature(), Curvature.CONCAVE)
        assert_equals(Sqrt(self.aff_exp).sign(), Sign.POSITIVE)
        assert_equals(Sqrt(self.cvx_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Sqrt(Constant(-2)).sign(), Sign.NEGATIVE)

        assert_equals(len(Sqrt(self.cvx_pos).arguments()), 1)
        assert_not_equals(Sqrt(self.cvx_pos).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_log_normcdf(self):
        assert_equals(Log_normcdf(self.conc_exp).curvature(), Curvature.CONCAVE)
        assert_equals(Log_normcdf(self.cvx_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Log_normcdf(self.cvx_exp).sign(), Sign.UNKNOWN)

        assert_equals(len(Log_normcdf(self.cvx_exp).arguments()), 1)
        assert_not_equals(Log_normcdf(self.cvx_exp).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_exp(self):
        assert_equals(Exp(self.cvx_exp).curvature(), Curvature.CONVEX)
        assert_equals(Exp(self.conc_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Exp(self.cvx_exp).sign(), Sign.POSITIVE)

        assert_equals(len(Exp(self.cvx_exp).arguments()), 1)
        assert_not_equals(Exp(self.cvx_exp).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_norm(self):
        assert_equals(Norm(self.cvx_pos, self.aff_exp, self.const_exp, 1341.143).curvature(), Curvature.CONVEX)
        assert_equals(Norm(self.cvx_pos, self.aff_exp, self.const_exp, 2).sign(), Sign.POSITIVE)

        assert_equals(Norm(self.conc_neg, 'Inf').curvature(), Curvature.CONVEX)
        assert_equals(Norm(self.cvx_neg, 'Inf').curvature(), Curvature.NONCONVEX)

        assert_equals(len(Norm(self.cvx_pos, self.cvx_neg, 10).arguments()), 2)
        assert_not_equals(Norm(self.cvx_pos, self.cvx_neg, 10).arguments()[0].name, Atom.GENERATED_EXPRESSION)

        # Check error message
        try:
            Norm(Constant(-2), 0)
            assert False
        except Exception, e:
            assert_equals(str(e), "Invalid value '0' for p in norm(..., p).")

        # Check error message
        try:
            Norm(Constant(-2), 'not inf')
            assert False
        except Exception, e:
            assert_equals(str(e), "Invalid value 'not inf' for p in norm(..., p).")

        # Check error message
        try:
            Norm()
            assert False
        except Exception, e:
            assert_equals(str(e), "No arguments given to 'norm'.")

    def test_abs(self):
        assert_equals(Abs(self.aff_exp).curvature(), Curvature.CONVEX)
        assert_equals(Abs(self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Abs(self.cvx_neg).curvature(), Curvature.NONCONVEX)
        assert_equals(Abs(self.noncvx_exp).sign(), Sign.POSITIVE)

        assert_equals(len(Abs(self.noncvx_exp).arguments()), 1)
        assert_not_equals(Abs(self.noncvx_exp).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_berhu(self):
        assert_equals(Berhu(self.aff_exp).curvature(), Curvature.CONVEX)
        assert_equals(Berhu(self.conc_neg,3).curvature(), Curvature.CONVEX)
        assert_equals(Berhu(self.cvx_neg,2).curvature(), Curvature.NONCONVEX)
        assert_equals(Berhu(self.noncvx_exp).sign(), Sign.POSITIVE)

        assert_equals(len(Berhu(self.cvx_pos, 10).arguments()), 1)
        assert_not_equals(Berhu(self.cvx_pos, 10).arguments()[0].name, Atom.GENERATED_EXPRESSION)

        # Check error message
        try:
            Berhu(Constant(-2), 0)
            assert False
        except Exception, e:
            assert_equals(str(e), "Invalid value '0' for M in berhu(...,M).")

    def test_entr(self):
        assert_equals(Entr(self.aff_exp).curvature(), Curvature.CONCAVE)
        assert_equals(Entr(self.conc_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Entr(self.cvx_exp).sign(), Sign.UNKNOWN)

        assert_equals(len(Entr(self.cvx_pos).arguments()), 1)
        assert_not_equals(Entr(self.cvx_pos).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_huber(self):
        assert_equals(Huber(self.aff_exp).curvature(), Curvature.CONVEX)
        assert_equals(Huber(self.conc_neg,3).curvature(), Curvature.CONVEX)
        assert_equals(Huber(self.cvx_neg,2).curvature(), Curvature.NONCONVEX)
        assert_equals(Huber(self.noncvx_exp).sign(), Sign.POSITIVE)

        assert_equals(len(Huber(self.cvx_pos, 10).arguments()), 1)
        assert_not_equals(Huber(self.cvx_pos, 10).arguments()[0].name, Atom.GENERATED_EXPRESSION)

        # Check error message
        try:
            Huber(Constant(-2), 0)
            assert False
        except Exception, e:
            assert_equals(str(e), "Invalid value '0' for M in huber(...,M).")

    def test_huber_pos(self):
        assert_equals(Huber_pos(self.aff_exp).curvature(), Curvature.CONVEX)
        assert_equals(Huber_pos(self.conc_neg,3).curvature(), Curvature.CONSTANT)
        assert_equals(Huber_pos(self.cvx_exp,2).curvature(), Curvature.CONVEX)
        assert_equals(Huber_pos(self.noncvx_exp).sign(), Sign.POSITIVE)

        assert_equals(len(Huber_pos(self.cvx_pos, 10).arguments()), 1)
        assert_not_equals(Huber_pos(self.cvx_pos, 10).arguments()[0].name, Atom.GENERATED_EXPRESSION)

        # Check error message
        try:
            Huber_pos(Constant(-2), 0)
            assert False
        except Exception, e:
            assert_equals(str(e), "Invalid value '0' for M in huber_pos(...,M).")

    def test_huber_circ(self):
        assert_equals(Huber_circ(self.aff_exp, self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Huber_circ(self.conc_neg, self.cvx_neg, 3).curvature(), Curvature.NONCONVEX)
        assert_equals(Huber_circ(self.aff_exp, self.cvx_pos, 2).curvature(), Curvature.CONVEX)
        assert_equals(Huber_circ(self.noncvx_exp).sign(), Sign.POSITIVE)

        assert_equals(len(Huber_circ(self.conc_neg, self.cvx_neg, 3).arguments()), 2)
        assert_not_equals(Huber_circ(self.conc_neg, self.cvx_neg, 3).arguments()[0].name, Atom.GENERATED_EXPRESSION)

        # Check error message
        try:
            Huber_circ(Constant(-2), 0)
            assert False
        except Exception, e:
            assert_equals(str(e), "Invalid value '0' for M in huber_circ(...,M).")

    def test_inv_pos(self):
        assert_equals(Inv_pos(self.cvx_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Inv_pos(self.conc_exp).curvature(), Curvature.CONVEX)

        assert_equals(len(Inv_pos(self.cvx_pos).arguments()), 1)
        assert_not_equals(Inv_pos(self.cvx_pos).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_kl_div(self):
        assert_equals(Kl_div(self.aff_exp, self.aff_exp).curvature(), Curvature.CONVEX)
        assert_equals(Kl_div(self.conc_exp, self.const_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Kl_div(self.cvx_exp, self.noncvx_exp).sign(), Sign.UNKNOWN)

        assert_equals(len(Kl_div(self.cvx_exp, self.noncvx_exp).arguments()), 2)
        assert_not_equals(Kl_div(self.cvx_exp, self.noncvx_exp).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_norm_largest(self):
        assert_equals(Norm_largest(self.cvx_pos, self.aff_exp, self.conc_neg, 2).curvature(), Curvature.CONVEX)
        assert_equals(Norm_largest(self.cvx_pos, self.aff_exp, self.const_exp, 2).sign(), Sign.POSITIVE)

        assert_equals(Norm_largest(self.conc_pos, 1).curvature(), Curvature.NONCONVEX)

        assert_equals(len(Norm_largest(self.cvx_pos, self.aff_exp, self.const_exp, 2).arguments()), 3)
        assert_not_equals(Norm_largest(self.cvx_pos, self.aff_exp, self.const_exp, 2).arguments()[0].name, Atom.GENERATED_EXPRESSION)

        # Check error message
        try:
            Norm_largest(Constant(-2), 'invalid')
            assert False
        except Exception, e:
            assert_equals(str(e), "Invalid value 'invalid' for k in norm_largest(...,k).")

    def test_pos(self):
        assert_equals(Pos(self.conc_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Pos(self.conc_neg).curvature(), Curvature.CONSTANT)
        assert_equals(Pos(self.cvx_exp).curvature(), Curvature.CONVEX)
        assert_equals(Pos(self.cvx_pos).sign(), Sign.POSITIVE)

        assert_equals(len(Pos(self.cvx_pos).arguments()), 1)
        assert_not_equals(Pos(self.cvx_pos).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_pow(self):
        assert_equals(Pow(self.cvx_pos,-1).curvature(), Curvature.NONCONVEX)
        assert_equals(Pow(self.conc_neg,-1).curvature(), Curvature.CONVEX)
        assert_equals(Pow(self.cvx_pos,-1).sign(), Sign.POSITIVE)

        assert_equals(Pow(self.cvx_pos,0.5).curvature(), Curvature.NONCONVEX)
        assert_equals(Pow(self.cvx_pos,0.5).sign(), Sign.POSITIVE)
        assert_equals(Pow(self.noncvx_exp, 0.5).sign(), Sign.UNKNOWN)
        assert_equals(Pow(self.conc_neg,0.5).curvature(), Curvature.CONCAVE)
        assert_equals(Pow(self.conc_neg,0.5).sign(), Sign.NEGATIVE)

        assert_equals(Pow(self.cvx_pos,2).curvature(), Curvature.CONVEX)
        assert_equals(Pow(self.conc_neg,2).curvature(), Curvature.CONVEX)
        assert_equals(Pow(self.cvx_neg,2).curvature(), Curvature.NONCONVEX)
        assert_equals(Pow(self.conc_pos,2).curvature(), Curvature.NONCONVEX)
        assert_equals(Pow(self.noncvx_exp, 2).sign(), Sign.POSITIVE)

        assert_equals(len(Pow(self.cvx_pos,2).arguments()), 1)
        assert_not_equals(Pow(self.cvx_pos,2).arguments()[0].name, Atom.GENERATED_EXPRESSION)

        # Check error message
        try:
            Pow(Constant(-2), 'wrong')
            assert False
        except Exception, e:
            assert_equals(str(e), "Invalid value 'wrong' for p in pow(..., p).")

    def test_pow_abs(self):
        assert_equals(Pow_abs(self.cvx_pos,2).curvature(), Curvature.CONVEX)
        assert_equals(Pow_abs(self.conc_neg,2).curvature(), Curvature.CONVEX)
        assert_equals(Pow_abs(self.cvx_neg,2).curvature(), Curvature.NONCONVEX)
        assert_equals(Pow_abs(self.conc_pos,2).curvature(), Curvature.NONCONVEX)
        assert_equals(Pow_abs(self.noncvx_exp, 2).sign(), Sign.POSITIVE)

        assert_equals(len(Pow_abs(self.cvx_pos,2).arguments()), 1)
        assert_not_equals(Pow_abs(self.cvx_pos,2).arguments()[0].name, Atom.GENERATED_EXPRESSION)

        # Check error message
        try:
            Pow_abs(Constant(-2), 0)
            assert False
        except Exception, e:
            assert_equals(str(e), 'Must have p >= 1 for pow_abs(..., p), but have p = 0.')
        
    def test_pow_pos(self):
        assert_equals(Pow_pos(self.cvx_pos,2).curvature(), Curvature.CONVEX)
        assert_equals(Pow_pos(self.conc_neg,2).curvature(), Curvature.CONSTANT)
        assert_equals(Pow_pos(self.conc_pos,2).curvature(), Curvature.NONCONVEX)
        assert_equals(Pow_pos(self.noncvx_exp, 2).sign(), Sign.POSITIVE)

        assert_equals(len(Pow_pos(self.cvx_pos,2).arguments()), 1)
        assert_not_equals(Pow_pos(self.cvx_pos,2).arguments()[0].name, Atom.GENERATED_EXPRESSION)

        # Check error message
        try:
            Pow_pos(Constant(-2), 0)
            assert False
        except Exception, e:
            assert_equals(str(e), 'Must have p >= 1 for pow_pos(..., p), but have p = 0.')

    def test_square_abs(self):
        assert_equals(Square_abs(self.cvx_pos).curvature(), Curvature.CONVEX)
        assert_equals(Square_abs(self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Square_abs(self.conc_pos).curvature(), Curvature.NONCONVEX)
        assert_equals(Square_abs(self.noncvx_exp).sign(), Sign.POSITIVE)

        assert_equals(len(Square_abs(self.cvx_pos).arguments()), 1)
        assert_not_equals(Square_abs(self.cvx_pos).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_square_pos(self):
        assert_equals(Square_pos(self.cvx_exp).curvature(), Curvature.CONVEX)
        assert_equals(Square_pos(self.conc_neg).curvature(), Curvature.CONSTANT)
        assert_equals(Square_pos(self.conc_pos).curvature(), Curvature.NONCONVEX)
        assert_equals(Square_pos(self.noncvx_exp).sign(), Sign.POSITIVE)

        assert_equals(len(Square_pos(self.cvx_pos).arguments()), 1)
        assert_not_equals(Square_pos(self.cvx_pos).arguments()[0].name, Atom.GENERATED_EXPRESSION)
        
    def test_rel_entr(self):
        assert_equals(Rel_entr(self.aff_exp, self.const_exp).curvature(), Curvature.CONVEX)
        assert_equals(Rel_entr(self.conc_exp, self.aff_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Rel_entr(self.cvx_exp, self.noncvx_exp).sign(), Sign.UNKNOWN)

        assert_equals(len(Rel_entr(self.aff_exp, self.const_exp).arguments()), 2)
        assert_not_equals(Rel_entr(self.aff_exp, self.const_exp).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_quad_over_lin(self):
        assert_equals(Quad_over_lin(self.cvx_pos, self.conc_exp).curvature(), Curvature.CONVEX)
        assert_equals(Quad_over_lin(self.cvx_pos, self.conc_exp).curvature(), Curvature.CONVEX)
        assert_equals(Quad_over_lin(self.conc_neg, self.cvx_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Quad_over_lin(self.cvx_exp, self.conc_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Quad_over_lin(self.noncvx_exp, self.conc_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Quad_over_lin(self.noncvx_exp, self.conc_exp).sign(), Sign.POSITIVE)

        assert_equals(len(Quad_over_lin(self.noncvx_exp, self.conc_exp).arguments()), 2)
        assert_not_equals(Quad_over_lin(self.noncvx_exp, self.cvx_pos).arguments()[0].name, Atom.GENERATED_EXPRESSION)

        # Check error message
        try:
            Quad_over_lin(self.cvx_pos, self.cvx_neg)
            assert False
        except Exception, e:
            assert_equals(str(e), 'quad_over_lin does not accept negative divisor arguments.')

    def test_sum_square(self):
        assert_equals(Sum_square(self.cvx_pos, self.aff_exp, self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Sum_square(self.cvx_neg, self.aff_exp, self.conc_neg).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square(self.conc_neg, self.cvx_exp).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square(self.cvx_neg, self.conc_neg).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square(self.noncvx_exp, self.cvx_pos).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square(self.noncvx_exp, self.cvx_pos).sign(), Sign.POSITIVE)

        assert_equals(len(Sum_square(self.cvx_pos, self.aff_exp, self.conc_neg).arguments()), 3)
        assert_not_equals(Sum_square(self.cvx_pos, self.aff_exp, self.conc_neg).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_sum_square_abs(self):
        assert_equals(Sum_square_abs(self.cvx_pos, self.aff_exp, self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Sum_square_abs(self.cvx_neg, self.aff_exp, self.conc_neg).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square_abs(self.conc_neg, self.cvx_neg).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square_abs(self.noncvx_exp, self.cvx_pos).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square_abs(self.noncvx_exp, self.cvx_pos).sign(), Sign.POSITIVE)

        assert_equals(len(Sum_square_abs(self.cvx_pos, self.aff_exp, self.conc_neg).arguments()), 3)
        assert_not_equals(Sum_square_abs(self.cvx_pos, self.aff_exp, self.conc_neg).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_sum_square_pos(self):
        assert_equals(Sum_square_pos(self.cvx_pos, self.aff_exp, self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Sum_square_pos(self.cvx_neg, self.aff_exp, self.conc_neg).curvature(), Curvature.CONVEX)
        assert_equals(Sum_square_pos(self.conc_neg, self.cvx_neg).curvature(), Curvature.CONSTANT)
        assert_equals(Sum_square_pos(self.conc_neg, self.cvx_neg).sign(), Sign.ZERO)
        assert_equals(Sum_square_pos(self.noncvx_exp, self.cvx_pos).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_square_pos(self.noncvx_exp, self.cvx_pos).sign(), Sign.POSITIVE)

        assert_equals(len(Sum_square_pos(self.cvx_pos, self.aff_exp, self.conc_neg).arguments()), 3)
        assert_not_equals(Sum_square_pos(self.cvx_pos, self.aff_exp, self.conc_neg).arguments()[0].name, Atom.GENERATED_EXPRESSION)

    def test_sum_largest(self):
        assert_equals(Sum_largest(self.cvx_pos, self.aff_exp, 2).curvature(), Curvature.CONVEX)
        assert_equals(Sum_largest(self.cvx_pos, self.aff_exp, 2).sign(), Sign.UNKNOWN)

        assert_equals(Sum_largest(self.conc_exp, 1).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_largest(self.cvx_exp, self.noncvx_exp, 1).curvature(), Curvature.NONCONVEX)

        assert_equals(len(Sum_largest(self.cvx_pos, self.aff_exp, self.conc_neg, 2).arguments()), 3)
        assert_not_equals(Sum_largest(self.cvx_pos, self.aff_exp, self.conc_neg, 2).arguments()[0].name, Atom.GENERATED_EXPRESSION)

        # Check error message
        try:
            Sum_largest(self.cvx_pos, 'invalid')
            assert False
        except Exception, e:
            assert_equals(str(e), "Invalid value 'invalid' for k in sum_largest(...,k).")

    def test_sum_smallest(self):
        assert_equals(Sum_smallest(self.cvx_exp, self.aff_exp, 2).curvature(), Curvature.NONCONVEX)
        assert_equals(Sum_smallest(self.cvx_exp, self.aff_exp, 2).sign(), Sign.UNKNOWN)

        assert_equals(Sum_smallest(self.conc_exp, 1).curvature(), Curvature.CONCAVE)
        assert_equals(Sum_smallest(self.conc_exp, self.noncvx_exp, 1).curvature(), Curvature.NONCONVEX)

        assert_equals(len(Sum_smallest(self.cvx_pos, self.aff_exp, self.conc_neg, 2).arguments()), 3)
        assert_not_equals(Sum_smallest(self.cvx_pos, self.aff_exp, self.conc_neg, 2).arguments()[0].name, Atom.GENERATED_EXPRESSION)

        # Check error message
        try:
            Sum_smallest(self.cvx_pos, 'invalid')
            assert False
        except Exception, e:
            assert_equals(str(e), "Invalid value 'invalid' for k in sum_smallest(...,k).")