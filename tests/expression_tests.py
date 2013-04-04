from dcp_parser.expression.vexity import Vexity
from dcp_parser.expression.sign import Sign
from dcp_parser.expression.expression import *
from nose.tools import assert_equals

class TestExpression(object):
    """ Unit tests for the expression/expression module. """
    @classmethod
    def setup_class(self):
        self.constant = Vexity(Vexity.CONSTANT_KEY)
        self.affine = Vexity(Vexity.AFFINE_KEY)
        self.convex = Vexity(Vexity.CONVEX_KEY)
        self.concave = Vexity(Vexity.CONCAVE_KEY)
        self.nonconvex = Vexity(Vexity.NONCONVEX_KEY)

        self.positive = Sign(Sign.POSITIVE_KEY)
        self.negative = Sign(Sign.NEGATIVE_KEY)
        self.unknown = Sign(Sign.UNKNOWN_KEY)
        self.zero = Sign(Sign.ZERO_KEY)

        self.pos_const = Expression(self.constant, self.positive, 'pos_const', [])
        self.neg_const = Expression(self.constant, self.negative, 'neg_const', [])
        self.zero_const = Expression(self.constant, self.zero, 'zero_const', [])
        self.unknown_const = Expression(self.constant, self.unknown, 'unknown_const', [])

        self.aff_exp = Expression(self.affine, self.unknown, 'aff_exp', [])
        self.cvx_exp = Expression(self.convex, self.unknown, 'convex_exp', [])
        self.conc_exp = Expression(self.concave, self.unknown, 'conc_exp', [])
        self.noncvx_exp = Expression(self.nonconvex, self.unknown, 'noncvx_exp', [])

    # Test sign behavior over addition, subtraction, and negation.
    def test_sign(self):
        assert_equals((self.pos_const - self.neg_const).sign, self.positive)
        assert_equals((self.neg_const - self.zero_const).sign, self.negative)
        assert_equals((self.pos_const + self.pos_const).sign, self.positive)
        assert_equals((self.zero_const + self.unknown_const).sign, self.unknown)
        assert_equals((-self.pos_const).sign, self.negative)

    # Text vexity behavior for arithmetic operations.
    def test_add(self):
        assert_equals((self.cvx_exp + self.cvx_exp).vexity, self.convex)
        assert_equals((self.noncvx_exp + self.conc_exp).vexity, self.nonconvex)
        assert_equals((self.cvx_exp + self.conc_exp).vexity, self.nonconvex)
        assert_equals((self.cvx_exp + self.cvx_exp).vexity, self.convex)
        assert_equals((self.aff_exp + self.conc_exp).vexity, self.concave)

    def test_sub(self):
        assert_equals((self.cvx_exp - self.cvx_exp).vexity, self.nonconvex)
        assert_equals((self.noncvx_exp - self.conc_exp).vexity, self.nonconvex)
        assert_equals((self.cvx_exp - self.conc_exp).vexity, self.convex)
        assert_equals((self.cvx_exp - self.cvx_exp).vexity, self.nonconvex)
        assert_equals((self.aff_exp - self.conc_exp).vexity, self.convex)

    def test_mult(self):
        assert_equals((self.pos_const * self.cvx_exp).vexity, self.convex)
        assert_equals((self.conc_exp * self.neg_const).vexity, self.convex)
        assert_equals((self.aff_exp * self.conc_exp).vexity, self.nonconvex)
        assert_equals((self.aff_exp * self.neg_const).vexity, self.affine)
        assert_equals((self.zero_const * self.noncvx_exp).vexity, self.constant)

    def test_div(self):
        assert_equals((self.cvx_exp / self.neg_const).vexity, self.concave)
        assert_equals((self.aff_exp / self.pos_const).vexity, self.affine)
        assert_equals((self.zero_const / self.conc_exp).vexity, self.constant)
        assert_equals((self.aff_exp / self.aff_exp).vexity, self.nonconvex)

    def test_neg(self):
        assert_equals((-self.cvx_exp).vexity, self.concave)
        assert_equals((-self.aff_exp).vexity, self.affine)

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

