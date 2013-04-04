from dcp_parser.expression.vexity import Vexity
from dcp_parser.expression.sign import Sign
from nose.tools import assert_equals

class TestVexity(object):
    """ Unit tests for the expression/vexity class. """
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

    def test_add(self):
        assert_equals(self.constant + self.convex, self.convex)
        assert_equals(self.nonconvex + self.concave, self.nonconvex)
        assert_equals(self.convex + self.concave, self.nonconvex)
        assert_equals(self.convex + self.convex, self.convex)
        assert_equals(self.affine + self.concave, self.concave)

    def test_sub(self):
        assert_equals(self.constant - self.convex, self.concave)
        assert_equals(self.nonconvex - self.concave, self.nonconvex)
        assert_equals(self.convex - self.concave, self.convex)
        assert_equals(self.convex - self.convex, self.nonconvex)
        assert_equals(self.affine - self.concave, self.convex)

    def test_mult(self):
        assert_equals(self.constant * self.convex, self.convex)
        assert_equals(self.constant * self.affine, self.affine)
        assert_equals(self.affine * self.concave, self.nonconvex)

    def test_div(self):
      assert_equals(self.convex / self.constant, self.convex)
      assert_equals(self.affine / self.constant, self.affine)
      assert_equals(self.constant / self.concave, self.nonconvex)

    def test_neg(self):
      assert_equals(-self.convex, self.concave)
      assert_equals(-self.affine, self.affine)

    def test_sign_mult(self):
      assert_equals(self.convex.sign_mult(self.positive), self.convex)
      assert_equals(self.concave.sign_mult(self.negative), self.convex)
      assert_equals(self.affine.sign_mult(self.unknown), self.affine)
      assert_equals(self.constant.sign_mult(self.negative), self.constant)
      assert_equals(self.convex.sign_mult(self.zero), self.constant)
      assert_equals(self.concave.sign_mult(self.unknown), self.nonconvex)
