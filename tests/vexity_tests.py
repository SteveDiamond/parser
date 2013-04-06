from dcp_parser.expression.vexity import Vexity
from dcp_parser.expression.sign import Sign
from nose.tools import assert_equals

class TestVexity(object):
    """ Unit tests for the expression/vexity class. """
    @classmethod
    def setup_class(self):
        pass

    def test_add(self):
        assert_equals(Vexity.CONSTANT + Vexity.CONVEX, Vexity.CONVEX)
        assert_equals(Vexity.NONCONVEX + Vexity.CONCAVE, Vexity.NONCONVEX)
        assert_equals(Vexity.CONVEX + Vexity.CONCAVE, Vexity.NONCONVEX)
        assert_equals(Vexity.CONVEX + Vexity.CONVEX, Vexity.CONVEX)
        assert_equals(Vexity.AFFINE + Vexity.CONCAVE, Vexity.CONCAVE)

    def test_sub(self):
        assert_equals(Vexity.CONSTANT - Vexity.CONVEX, Vexity.CONCAVE)
        assert_equals(Vexity.NONCONVEX - Vexity.CONCAVE, Vexity.NONCONVEX)
        assert_equals(Vexity.CONVEX - Vexity.CONCAVE, Vexity.CONVEX)
        assert_equals(Vexity.CONVEX - Vexity.CONVEX, Vexity.NONCONVEX)
        assert_equals(Vexity.AFFINE - Vexity.CONCAVE, Vexity.CONVEX)

    def test_mult(self):
        assert_equals(Vexity.CONSTANT * Vexity.CONVEX, Vexity.CONVEX)
        assert_equals(Vexity.CONSTANT * Vexity.AFFINE, Vexity.AFFINE)
        assert_equals(Vexity.AFFINE * Vexity.CONCAVE, Vexity.NONCONVEX)

    def test_div(self):
        assert_equals(Vexity.CONVEX / Vexity.CONSTANT, Vexity.CONVEX)
        assert_equals(Vexity.AFFINE / Vexity.CONSTANT, Vexity.AFFINE)
        assert_equals(Vexity.CONSTANT / Vexity.CONCAVE, Vexity.NONCONVEX)

    def test_neg(self):
        assert_equals(-Vexity.CONVEX, Vexity.CONCAVE)
        assert_equals(-Vexity.AFFINE, Vexity.AFFINE)

    def test_sign_mult(self):
        assert_equals(Vexity.CONVEX.sign_mult(Sign.POSITIVE), Vexity.CONVEX)
        assert_equals(Vexity.CONCAVE.sign_mult(Sign.NEGATIVE), Vexity.CONVEX)
        assert_equals(Vexity.AFFINE.sign_mult(Sign.UNKNOWN), Vexity.AFFINE)
        assert_equals(Vexity.CONSTANT.sign_mult(Sign.NEGATIVE), Vexity.CONSTANT)
        assert_equals(Vexity.CONVEX.sign_mult(Sign.ZERO), Vexity.CONSTANT)
        assert_equals(Vexity.CONCAVE.sign_mult(Sign.UNKNOWN), Vexity.NONCONVEX)
