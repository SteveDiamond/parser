from dcp_parser.expression.vexity import Vexity
from dcp_parser.atomic.monotonicity import Monotonicity
from nose.tools import *

class TestMonotonicity(object):
    """ Unit tests for the atomic/monotonicity class. """
    @classmethod
    def setup_class(self):
        pass

    # Test application of DCP composition rules to determine vexity.
    def test_dcp_vexity(self):
        assert_equals(Monotonicity.INCREASING.dcp_vexity(Vexity.AFFINE, Vexity.CONVEX), Vexity.CONVEX)
        assert_equals(Monotonicity.NONMONOTONIC.dcp_vexity(Vexity.AFFINE, Vexity.AFFINE), Vexity.AFFINE)
        assert_equals(Monotonicity.DECREASING.dcp_vexity(Vexity.NONCONVEX, Vexity.CONSTANT), Vexity.CONSTANT)

        assert_equals(Monotonicity.INCREASING.dcp_vexity(Vexity.CONVEX, Vexity.CONVEX), Vexity.CONVEX)
        assert_equals(Monotonicity.DECREASING.dcp_vexity(Vexity.CONVEX, Vexity.CONCAVE), Vexity.CONVEX)

        assert_equals(Monotonicity.INCREASING.dcp_vexity(Vexity.CONCAVE, Vexity.CONCAVE), Vexity.CONCAVE)
        assert_equals(Monotonicity.DECREASING.dcp_vexity(Vexity.CONCAVE, Vexity.CONVEX), Vexity.CONCAVE)

        assert_equals(Monotonicity.INCREASING.dcp_vexity(Vexity.CONCAVE, Vexity.CONVEX), Vexity.NONCONVEX)
        assert_equals(Monotonicity.NONMONOTONIC.dcp_vexity(Vexity.CONCAVE, Vexity.AFFINE), Vexity.CONCAVE)