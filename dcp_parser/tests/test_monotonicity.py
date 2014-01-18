from dcp_parser.expression.curvature import Curvature
from dcp_parser.atomic.monotonicity import Monotonicity
from nose.tools import *

class TestMonotonicity(object):
    """ Unit tests for the atomic/monotonicity class. """
    @classmethod
    def setup_class(self):
        pass

    # Test application of DCP composition rules to determine curvature.
    def test_dcp_curvature(self):
        assert_equals(Monotonicity.INCREASING.dcp_curvature(Curvature.AFFINE, Curvature.CONVEX), Curvature.CONVEX)
        assert_equals(Monotonicity.NONMONOTONIC.dcp_curvature(Curvature.AFFINE, Curvature.AFFINE), Curvature.AFFINE)
        assert_equals(Monotonicity.DECREASING.dcp_curvature(Curvature.NONCONVEX, Curvature.CONSTANT), Curvature.NONCONVEX)

        assert_equals(Monotonicity.INCREASING.dcp_curvature(Curvature.CONVEX, Curvature.CONVEX), Curvature.CONVEX)
        assert_equals(Monotonicity.DECREASING.dcp_curvature(Curvature.CONVEX, Curvature.CONCAVE), Curvature.CONVEX)

        assert_equals(Monotonicity.INCREASING.dcp_curvature(Curvature.CONCAVE, Curvature.CONCAVE), Curvature.CONCAVE)
        assert_equals(Monotonicity.DECREASING.dcp_curvature(Curvature.CONCAVE, Curvature.CONVEX), Curvature.CONCAVE)

        assert_equals(Monotonicity.INCREASING.dcp_curvature(Curvature.CONCAVE, Curvature.CONVEX), Curvature.NONCONVEX)
        assert_equals(Monotonicity.NONMONOTONIC.dcp_curvature(Curvature.CONCAVE, Curvature.AFFINE), Curvature.CONCAVE)

        assert_equals(Monotonicity.NONMONOTONIC.dcp_curvature(Curvature.CONSTANT, Curvature.NONCONVEX), Curvature.CONSTANT)