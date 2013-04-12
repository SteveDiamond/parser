from dcp_parser.expression.sign import Sign
from nose.tools import *

class TestSign(object):
  """ Unit tests for the expression/sign class. """
  @classmethod
  def setup_class(self):
      pass
      
  def test_add(self):
      assert_equals(Sign.POSITIVE + Sign.NEGATIVE, Sign.UNKNOWN)
      assert_equals(Sign.NEGATIVE + Sign.ZERO, Sign.NEGATIVE)
      assert_equals(Sign.POSITIVE + Sign.POSITIVE, Sign.POSITIVE)
      assert_equals(Sign.UNKNOWN + Sign.ZERO, Sign.UNKNOWN)

  def test_sub(self):
      assert_equals(Sign.POSITIVE - Sign.NEGATIVE, Sign.POSITIVE)
      assert_equals(Sign.NEGATIVE - Sign.ZERO, Sign.NEGATIVE)
      assert_equals(Sign.POSITIVE - Sign.POSITIVE, Sign.UNKNOWN)

  def test_mult(self):
      assert_equals(Sign.ZERO * Sign.POSITIVE, Sign.ZERO)
      assert_equals(Sign.UNKNOWN * Sign.POSITIVE, Sign.UNKNOWN)
      assert_equals(Sign.POSITIVE * Sign.NEGATIVE, Sign.NEGATIVE)
      assert_equals(Sign.NEGATIVE * Sign.NEGATIVE, Sign.POSITIVE)
      assert_equals(Sign.ZERO * Sign.UNKNOWN, Sign.ZERO)

  def test_neg(self):
      assert_equals(-Sign.ZERO, Sign.ZERO)
      assert_equals(-Sign.POSITIVE, Sign.NEGATIVE)

  def test_div(self):
      assert_equals(Sign.POSITIVE / Sign.NEGATIVE, Sign.NEGATIVE)

  @raises(Exception)
  def test_div_by_zero(self):
      Sign.POSITIVE / Sign.ZERO

  # Test < and >
  def test_cmp(self):
     assert Sign.POSITIVE > Sign.UNKNOWN
     assert Sign.NEGATIVE < Sign.ZERO
     assert Sign.ZERO < Sign.UNKNOWN
     assert not Sign.ZERO > Sign.ZERO
     assert not Sign.POSITIVE < Sign.ZERO

    # Test <= and =>
  def test_cmp_eq(self):
     assert Sign.POSITIVE >= Sign.POSITIVE
     assert Sign.NEGATIVE <= Sign.ZERO
     assert Sign.ZERO <= Sign.UNKNOWN
     assert not Sign.UNKNOWN <= Sign.ZERO
     assert not Sign.POSITIVE <= Sign.ZERO