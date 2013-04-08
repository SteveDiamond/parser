from dcp_parser.expression.curvature import Curvature
from dcp_parser.expression.sign import Sign
from nose.tools import assert_equals

class TestCurvature(object):
    """ Unit tests for the expression/curvature class. """
    @classmethod
    def setup_class(self):
        pass

    def test_add(self):
        assert_equals(Curvature.CONSTANT + Curvature.CONVEX, Curvature.CONVEX)
        assert_equals(Curvature.NONCONVEX + Curvature.CONCAVE, Curvature.NONCONVEX)
        assert_equals(Curvature.CONVEX + Curvature.CONCAVE, Curvature.NONCONVEX)
        assert_equals(Curvature.CONVEX + Curvature.CONVEX, Curvature.CONVEX)
        assert_equals(Curvature.AFFINE + Curvature.CONCAVE, Curvature.CONCAVE)

    def test_sub(self):
        assert_equals(Curvature.CONSTANT - Curvature.CONVEX, Curvature.CONCAVE)
        assert_equals(Curvature.NONCONVEX - Curvature.CONCAVE, Curvature.NONCONVEX)
        assert_equals(Curvature.CONVEX - Curvature.CONCAVE, Curvature.CONVEX)
        assert_equals(Curvature.CONVEX - Curvature.CONVEX, Curvature.NONCONVEX)
        assert_equals(Curvature.AFFINE - Curvature.CONCAVE, Curvature.CONVEX)

    def test_mult(self):
        assert_equals(Curvature.CONSTANT * Curvature.CONVEX, Curvature.CONVEX)
        assert_equals(Curvature.CONSTANT * Curvature.AFFINE, Curvature.AFFINE)
        assert_equals(Curvature.AFFINE * Curvature.CONCAVE, Curvature.NONCONVEX)

    def test_div(self):
        assert_equals(Curvature.CONVEX / Curvature.CONSTANT, Curvature.CONVEX)
        assert_equals(Curvature.AFFINE / Curvature.CONSTANT, Curvature.AFFINE)
        assert_equals(Curvature.CONSTANT / Curvature.CONCAVE, Curvature.NONCONVEX)

    def test_neg(self):
        assert_equals(-Curvature.CONVEX, Curvature.CONCAVE)
        assert_equals(-Curvature.AFFINE, Curvature.AFFINE)

    def test_sign_mult(self):
        assert_equals(Curvature.CONVEX.sign_mult(Sign.POSITIVE), Curvature.CONVEX)
        assert_equals(Curvature.CONCAVE.sign_mult(Sign.NEGATIVE), Curvature.CONVEX)
        assert_equals(Curvature.AFFINE.sign_mult(Sign.UNKNOWN), Curvature.AFFINE)
        assert_equals(Curvature.CONSTANT.sign_mult(Sign.NEGATIVE), Curvature.CONSTANT)
        assert_equals(Curvature.CONVEX.sign_mult(Sign.ZERO), Curvature.CONSTANT)
        assert_equals(Curvature.CONCAVE.sign_mult(Sign.UNKNOWN), Curvature.NONCONVEX)
