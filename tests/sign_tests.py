from dcp_parser.expression.sign import Sign
from nose.tools import *

class TestSign(object):
  """ Unit tests for the expression/sign class. """
  @classmethod
  def setup_class(self):
      self.positive = Sign(Sign.POSITIVE_KEY)
      self.negative = Sign(Sign.NEGATIVE_KEY)
      self.unknown = Sign(Sign.UNKNOWN_KEY)
      self.zero = Sign(Sign.ZERO_KEY)

  def test_add(self):
      assert_equals(self.positive + self.negative, self.unknown)
      assert_equals(self.negative + self.zero, self.negative)
      assert_equals(self.positive + self.positive, self.positive)
      assert_equals(self.unknown + self.zero, self.unknown)

  def test_sub(self):
      assert_equals(self.positive - self.negative, self.positive)
      assert_equals(self.negative - self.zero, self.negative)
      assert_equals(self.positive - self.positive, self.unknown)

  def test_mult(self):
      assert_equals(self.zero * self.positive, self.zero)
      assert_equals(self.unknown * self.positive, self.unknown)
      assert_equals(self.positive * self.negative, self.negative)
      assert_equals(self.negative * self.negative, self.positive)
      assert_equals(self.zero * self.unknown, self.zero)

  def test_neg(self):
      assert_equals(-self.zero, self.zero)
      assert_equals(-self.positive, self.negative)

  def test_div(self):
      assert_equals(self.positive / self.negative, self.negative)

  @raises(Exception)
  def test_div_by_zero(self):
      self.positive / self.zero