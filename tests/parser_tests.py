from dcp_parser.parser import Parser
from dcp_parser.expression.vexity import Vexity
from dcp_parser.expression.sign import Sign
from dcp_parser.expression.expression import *
from nose.tools import assert_equals

class TestExpression(object):
      """ Unit tests for the parser/parser class. """
      def setup(self):
          self.parser = Parser()

          self.affine = Vexity(Vexity.AFFINE_KEY)
          self.constant = Vexity(Vexity.CONSTANT_KEY)

          self.positive = Sign(Sign.POSITIVE_KEY)
          self.negative = Sign(Sign.NEGATIVE_KEY)
          self.unknown = Sign(Sign.UNKNOWN_KEY)
          self.zero = Sign(Sign.ZERO_KEY)

      def test_parse_variables(self):
          exp = 'variable x'
          self.parser.parse(exp)
          assert 'x' in self.parser.symbol_table
          assert_equals(self.parser.symbol_table['x'].vexity, self.affine)

          exp = ' variable  y    z '
          self.parser.parse(exp)
          assert 'z' in self.parser.symbol_table
          assert len(self.parser.symbol_table.keys()) == 3

      def test_parse_parameters(self):
          exp = 'parameter x'
          self.parser.parse(exp)
          assert 'x' in self.parser.symbol_table
          assert_equals(self.parser.symbol_table['x'].vexity, self.constant)
          assert_equals(self.parser.symbol_table['x'].sign, self.unknown)

          exp = ' parameter negative  y    z '
          self.parser.parse(exp)
          assert 'z' in self.parser.symbol_table
          assert_equals(self.parser.symbol_table['z'].sign, self.negative)
          assert_equals(len(self.parser.symbol_table.keys()), 3)

      # Test parser with only variables and parameters
      def test_basic_eval(self):
          self.parser.parse('variable x y z')
          self.parser.parse('parameter positive a b')
          self.parser.parse('parameter zero c d')
          expression = 'c * (a * x + d * (y / b - z))'
          self.parser.parse(expression)

          result = self.parser.expressions[0]
          assert_equals(expression, str(result))
          assert_equals(result.vexity, self.constant)
          assert_equals(result.sign, self.zero)

          rh_exp = result.subexpressions[1]
          assert_equals('a * x + d * (y / b - z)', str(rh_exp))
          assert_equals(rh_exp.vexity, self.affine)