from dcp_parser.expression.vexity import Vexity
from dcp_parser.expression.sign import Sign
from dcp_parser.expression.expression import *
from nose.tools import assert_equals

class TestExpression(object):
    """ Unit tests for the expression/expression module. """
    @classmethod
    def setup_class(self):
        self.pos_const = Expression(Vexity.CONSTANT, Sign.POSITIVE, 'pos_const')
        self.neg_const = Expression(Vexity.CONSTANT, Sign.NEGATIVE, 'neg_const')
        self.zero_const = Expression(Vexity.CONSTANT, Sign.ZERO, 'zero_const')
        self.unknown_const = Expression(Vexity.CONSTANT, Sign.UNKNOWN, 'unknown_const')

        self.aff_exp = Expression(Vexity.AFFINE, Sign.UNKNOWN, 'aff_exp')
        self.cvx_exp = Expression(Vexity.CONVEX, Sign.UNKNOWN, 'convex_exp')
        self.conc_exp = Expression(Vexity.CONCAVE, Sign.UNKNOWN, 'conc_exp')
        self.noncvx_exp = Expression(Vexity.NONCONVEX, Sign.UNKNOWN, 'noncvx_exp')

    # Test sign behavior over addition, subtraction, and negation.
    def test_sign(self):
        assert_equals((self.pos_const - self.neg_const).sign, Sign.POSITIVE)
        assert_equals((self.neg_const - self.zero_const).sign, Sign.NEGATIVE)
        assert_equals((self.pos_const + self.pos_const).sign, Sign.POSITIVE)
        assert_equals((self.zero_const + self.unknown_const).sign, Sign.UNKNOWN)
        assert_equals((-self.pos_const).sign, Sign.NEGATIVE)

    # Text vexity behavior for arithmetic operations.
    def test_add(self):
        assert_equals((self.cvx_exp + self.cvx_exp).vexity, Vexity.CONVEX)
        assert_equals((self.noncvx_exp + self.conc_exp).vexity, Vexity.NONCONVEX)
        assert_equals((self.cvx_exp + self.conc_exp).vexity, Vexity.NONCONVEX)
        assert_equals((self.cvx_exp + self.cvx_exp).vexity, Vexity.CONVEX)
        assert_equals((self.aff_exp + self.conc_exp).vexity, Vexity.CONCAVE)

    def test_sub(self):
        assert_equals((self.cvx_exp - self.cvx_exp).vexity, Vexity.NONCONVEX)
        assert_equals((self.noncvx_exp - self.conc_exp).vexity, Vexity.NONCONVEX)
        assert_equals((self.cvx_exp - self.conc_exp).vexity, Vexity.CONVEX)
        assert_equals((self.cvx_exp - self.cvx_exp).vexity, Vexity.NONCONVEX)
        assert_equals((self.aff_exp - self.conc_exp).vexity, Vexity.CONVEX)

    def test_mult(self):
        assert_equals((self.pos_const * self.cvx_exp).vexity, Vexity.CONVEX)
        assert_equals((self.conc_exp * self.neg_const).vexity, Vexity.CONVEX)
        assert_equals((self.aff_exp * self.conc_exp).vexity, Vexity.NONCONVEX)
        assert_equals((self.aff_exp * self.neg_const).vexity, Vexity.AFFINE)
        assert_equals((self.zero_const * self.noncvx_exp).vexity, Vexity.CONSTANT)

    def test_div(self):
        assert_equals((self.cvx_exp / self.neg_const).vexity, Vexity.CONCAVE)
        assert_equals((self.aff_exp / self.pos_const).vexity, Vexity.AFFINE)
        assert_equals((self.zero_const / self.conc_exp).vexity, Vexity.CONSTANT)
        assert_equals((self.aff_exp / self.aff_exp).vexity, Vexity.NONCONVEX)

    def test_neg(self):
        assert_equals((-self.cvx_exp).vexity, Vexity.CONCAVE)
        assert_equals((-self.aff_exp).vexity, Vexity.AFFINE)

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

