from dcp_parser.parser import Parser
from dcp_parser.expression.curvature import Curvature
from dcp_parser.expression.sign import Sign
from dcp_parser.expression.expression import *
from nose.tools import assert_equals

class TestParser(object):
      """ Unit tests for the parser/parser class. """
      def setup(self):
          self.parser = Parser()

      def test_parse_variables(self):
          exp = 'variable x'
          self.parser.parse(exp)
          assert 'x' in self.parser.symbol_table
          assert_equals(self.parser.symbol_table['x'].curvature, Curvature.AFFINE)

          exp = ' variable  y    z '
          self.parser.parse(exp)
          assert 'z' in self.parser.symbol_table
          assert len(self.parser.symbol_table.keys()) == 3

      def test_parse_parameters(self):
          exp = 'parameter x'
          self.parser.parse(exp)
          assert 'x' in self.parser.symbol_table
          assert_equals(self.parser.symbol_table['x'].curvature, Curvature.CONSTANT)
          assert_equals(self.parser.symbol_table['x'].sign, Sign.UNKNOWN)

          exp = ' parameter negative  y    z '
          self.parser.parse(exp)
          assert 'z' in self.parser.symbol_table
          assert_equals(self.parser.symbol_table['z'].sign, Sign.NEGATIVE)
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
          assert_equals(result.curvature, Curvature.CONSTANT)
          assert_equals(result.sign, Sign.ZERO)

          rh_exp = result.subexpressions[1]
          assert_equals('a * x + d * (y / b - z)', str(rh_exp))
          assert_equals(rh_exp.curvature, Curvature.AFFINE)

      # Test parser with numeric constants
      def test_constants_eval(self):
          self.parser.parse('variable x y z')
          self.parser.parse('parameter negative a b')
          expression = '-2 * b + 0 * (z * x - 5) + -a / 1.5'
          self.parser.parse(expression)

          result = self.parser.expressions[0]
          assert_equals(expression, str(result))
          assert_equals(result.curvature, Curvature.CONSTANT)
          assert_equals(result.sign, Sign.POSITIVE)

      # Test parser with atoms
      def test_atoms_eval(self):
          self.parser.parse('variable u v')
          self.parser.parse('parameter positive c d')
          expression = 'c * square(square(u)) - log(v) - (-c * log_sum_exp(d, u, v) - max(u, c))'
          self.parser.parse(expression)

          result = self.parser.expressions[0]
          assert_equals(expression, str(result))
          assert_equals(result.curvature, Curvature.CONVEX)
          assert_equals(result.sign, Sign.UNKNOWN)

          expression = '-square(square(u)) - max(square(v), c)'
          self.parser.parse(expression)
          result = self.parser.expressions[1]
          assert_equals(expression, str(result))
          assert_equals(result.curvature, Curvature.CONCAVE)
          assert_equals(result.sign, Sign.NEGATIVE)

          expression = 'c * square(log(u)) + max(c, log_sum_exp(max(u, v), c))'
          self.parser.parse(expression)
          result = self.parser.expressions[2]
          assert_equals(expression, str(result))
          assert_equals(result.curvature, Curvature.NONCONVEX)
          assert_equals(result.sign, Sign.POSITIVE)