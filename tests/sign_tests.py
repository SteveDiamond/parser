from parser.expression.sign import Sign
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
      assert (self.positive + self.negative) == self.unknown
      assert (self.negative + self.zero) == self.negative
      assert (self.positive + self.positive) == self.positive
      assert (self.unknown + self.zero) == self.unknown

  def test_sub(self):
      assert (self.positive - self.negative) == self.positive
      assert (self.negative - self.zero) == self.negative
      assert (self.positive - self.positive) == self.unknown

  def test_mult(self):
      assert (self.zero * self.positive) == self.zero
      assert (self.unknown * self.positive) == self.unknown
      assert (self.positive * self.negative) == self.negative
      assert (self.negative * self.negative) == self.positive

  def test_neg(self):
      assert -self.zero == self.zero
      assert -self.positive == self.negative

  def test_div(self):
      assert self.positive / self.negative == self.negative

  @raises(Exception)
  def test_div_by_zero(self):
      self.positive / self.zero