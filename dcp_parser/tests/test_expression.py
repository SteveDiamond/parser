from dcp_parser.expression.curvature import Curvature
from dcp_parser.expression.sign import Sign
from dcp_parser.expression.expression import *
from nose.tools import assert_equals

class TestExpression(object):
    """ Unit tests for the expression/expression module. """
    @classmethod
    def setup_class(self):
        self.pos_const = Expression(Curvature.CONSTANT, Sign.POSITIVE, 'pos_const')
        self.neg_const = Expression(Curvature.CONSTANT, Sign.NEGATIVE, 'neg_const')
        self.zero_const = Expression(Curvature.CONSTANT, Sign.ZERO, 'zero_const')
        self.unknown_const = Expression(Curvature.CONSTANT, Sign.UNKNOWN, 'unknown_const')

        self.aff_exp = Expression(Curvature.AFFINE, Sign.UNKNOWN, 'aff_exp')
        self.cvx_exp = Expression(Curvature.CONVEX, Sign.UNKNOWN, 'convex_exp')
        self.conc_exp = Expression(Curvature.CONCAVE, Sign.UNKNOWN, 'conc_exp')
        self.noncvx_exp = Expression(Curvature.NONCONVEX, Sign.UNKNOWN, 'noncvx_exp')

    # Test sign behavior over addition, subtraction, and negation.
    def test_sign(self):
        assert_equals((self.pos_const - self.neg_const).sign, Sign.POSITIVE)
        assert_equals((self.neg_const - self.zero_const).sign, Sign.NEGATIVE)
        assert_equals((self.pos_const + self.pos_const).sign, Sign.POSITIVE)
        assert_equals((self.zero_const + self.unknown_const).sign, Sign.UNKNOWN)
        assert_equals((-self.pos_const).sign, Sign.NEGATIVE)

    # Text curvature behavior for arithmetic operations.
    def test_add(self):
        assert_equals((self.cvx_exp + self.cvx_exp).curvature, Curvature.CONVEX)
        assert_equals((self.noncvx_exp + self.conc_exp).curvature, Curvature.NONCONVEX)
        assert_equals((self.cvx_exp + self.conc_exp).curvature, Curvature.NONCONVEX)
        assert_equals((self.cvx_exp + self.cvx_exp).curvature, Curvature.CONVEX)
        assert_equals((self.aff_exp + self.conc_exp).curvature, Curvature.CONCAVE)

    def test_sub(self):
        assert_equals((self.cvx_exp - self.cvx_exp).curvature, Curvature.NONCONVEX)
        assert_equals((self.noncvx_exp - self.conc_exp).curvature, Curvature.NONCONVEX)
        assert_equals((self.cvx_exp - self.conc_exp).curvature, Curvature.CONVEX)
        assert_equals((self.cvx_exp - self.cvx_exp).curvature, Curvature.NONCONVEX)
        assert_equals((self.aff_exp - self.conc_exp).curvature, Curvature.CONVEX)

    def test_mult(self):
        assert_equals((self.pos_const * self.cvx_exp).curvature, Curvature.CONVEX)
        assert_equals((self.conc_exp * self.neg_const).curvature, Curvature.CONVEX)
        assert_equals((self.aff_exp * self.conc_exp).curvature, Curvature.NONCONVEX)
        assert_equals((self.aff_exp * self.neg_const).curvature, Curvature.AFFINE)
        assert_equals((self.zero_const * self.noncvx_exp).curvature, Curvature.CONSTANT)

    def test_div(self):
        assert_equals((self.cvx_exp / self.neg_const).curvature, Curvature.CONCAVE)
        assert_equals((self.aff_exp / self.pos_const).curvature, Curvature.AFFINE)
        assert_equals((self.zero_const / self.conc_exp).curvature, Curvature.CONSTANT)
        assert_equals((self.aff_exp / self.aff_exp).curvature, Curvature.NONCONVEX)

    def test_neg(self):
        assert_equals((-self.cvx_exp).curvature, Curvature.CONCAVE)
        assert_equals((-self.aff_exp).curvature, Curvature.AFFINE)

    # Tests whether expression string representations properly reflect the
    # parenthesization of the original expression.
    def test_to_str(self):
        # Unequal priorities
        exp = (self.pos_const + self.neg_const) * self.zero_const
        expected_str = "(" + str(self.pos_const) + " + " + \
          str(self.neg_const) + ")" + " * " + str(self.zero_const)
        assert_equals(str(exp), expected_str)

        # Equal priorities
        exp = self.pos_const + (self.neg_const - self.zero_const)
        expected_str = str(self.pos_const) + " + " + \
          "(" + str(self.neg_const) + " - " + str(self.zero_const) + ")" 
        assert_equals(str(exp), expected_str)

        # Extraneous parentheses
        exp = (self.pos_const / self.neg_const) * self.zero_const
        expected_str = str(self.pos_const) + " / " + \
          str(self.neg_const) + " * " + str(self.zero_const)
        assert_equals(str(exp), expected_str)

    # Tests whether parent is overriden for variables
    # and parameters that are reused.
    def test_parent(self):
        x = Variable('x')
        a = Variable('a')
        exp1 = -a
        exp2 = a + x

        a1 = exp1.subexpressions[0]
        a2 = exp2.subexpressions[0]
        assert_equals(str(a1.parent), str(exp1))
        assert_equals(str(a2.parent), str(exp2))

        exp3 = x / x * x
        x1 = exp3.subexpressions[0].subexpressions[0]
        x2 = exp3.subexpressions[0].subexpressions[1]
        x3 = exp3.subexpressions[1]
        assert_equals(str(x1.parent), 'x / x')
        assert_equals(str(x2.parent), 'x / x')
        assert_equals(str(x3.parent), 'x / x * x')
