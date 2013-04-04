from parser.expression.vexity import Vexity
from parser.expression.sign import Sign

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
        assert (self.constant + self.convex) == self.convex
        assert (self.nonconvex + self.concave) == self.nonconvex
        assert (self.convex + self.concave) == self.nonconvex
        assert (self.convex + self.convex) == self.convex
        assert (self.affine + self.concave) == self.concave

    def test_sub(self):
        assert (self.constant - self.convex) == self.concave
        assert (self.nonconvex - self.concave) == self.nonconvex
        assert (self.convex - self.concave) == self.convex
        assert (self.convex - self.convex) == self.nonconvex
        assert (self.affine - self.concave) == self.convex

    def test_mult(self):
        assert (self.constant * self.convex) == self.convex
        assert (self.constant * self.affine) == self.affine
        assert (self.affine * self.concave) == self.nonconvex

    def test_div(self):
      assert (self.convex / self.constant) == self.convex
      assert (self.affine / self.constant) == self.affine
      assert (self.constant / self.concave) == self.nonconvex

    def test_neg(self):
      assert -self.convex == self.concave
      assert -self.affine == self.affine

    def test_sign_mult(self):
      assert self.convex.sign_mult(self.positive) == self.convex
      assert self.concave.sign_mult(self.negative) == self.convex
      assert self.affine.sign_mult(self.unknown) == self.affine
      assert self.constant.sign_mult(self.negative) == self.constant
      assert self.convex.sign_mult(self.zero) == self.constant
      assert self.concave.sign_mult(self.unknown) == self.nonconvex
