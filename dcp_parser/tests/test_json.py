from dcp_parser.expression.curvature import Curvature
from dcp_parser.expression.sign import Sign
from dcp_parser.expression.expression import *
from dcp_parser.expression.constraints import *
import dcp_parser.atomic.atom_loader as atom_loader
import json
import dcp_parser.json.settings as settings
from dcp_parser.json.statement_encoder import StatementEncoder
from nose.tools import assert_equals

class TestJson(object):
    """ Unit tests for the json module. """
    @classmethod
    def setup_class(self):
        self.pos_const = Expression(Curvature.CONSTANT, Sign.POSITIVE, 'pos_const')
        self.neg_const = Expression(Curvature.CONSTANT, Sign.NEGATIVE, 'neg_const')
        self.zero_const = Expression(Curvature.CONSTANT, Sign.ZERO, 'zero_const')
        self.unknown_const = Expression(Curvature.CONSTANT, Sign.UNKNOWN, 'unknown_const')

        self.aff_exp = Expression(Curvature.AFFINE, Sign.UNKNOWN, 'aff_exp')
        self.cvx_exp = Expression(Curvature.CONVEX, Sign.UNKNOWN, 'convex_exp')
        self.conc_exp = Expression(Curvature.CONCAVE, Sign.UNKNOWN, 'conc_exp')
        self.noncvx_exp = Expression(Curvature.NONCONVEX, Sign.UNKNOWN, 'noncvx_exp')

    # Tests the json encoding and decoding of expressions via the statement encoder.
    def test_expression_encoder(self):
        atom_dict = atom_loader.generate_atom_dict()
        exp = atom_dict['square'](self.conc_exp + self.cvx_exp)
        json_str = StatementEncoder().encode(exp)
        result = json.loads(json_str, object_hook=StatementEncoder.as_statement)
        assert_equals(result.name, exp.name)
        assert_equals(result.short_name, exp.short_name)
        assert_equals(result.curvature, exp.curvature)
        assert_equals(result.monotonicity, exp.monotonicity)
        assert_equals(result.sign, exp.sign)
        # subexpressions
        assert_equals(len(result.subexpressions), 1)
        assert_equals(result.subexpressions[0].name, exp.subexpressions[0].name)
        # errors
        for error in exp.errors:
            if error.is_indexed():
                assert_equals(result.json_errors['indexed_errors'][str(error.index)], error.error_message())
            else:
                assert error.error_message() in result.json_errors['unsorted_errors']

    # # Tests the json encoding and decoding and constraints via the statement encoder.
    def test_constraint_encoder(self):
        constraint = LeqConstraint(self.conc_exp, self.noncvx_exp)
        json_str = StatementEncoder().encode(constraint)
        #import pdb; pdb.set_trace()
        result = json.loads(json_str, object_hook=StatementEncoder.as_statement)
        assert_equals(str(result), str(constraint))
        assert_equals(result.short_name, constraint.short_name)
        assert_equals(result.CONSTRAINT_STR, constraint.CONSTRAINT_STR)
        # subexpressions
        assert_equals(result.lhs.name, constraint.subexpressions[0].name)
        assert_equals(result.rhs.name, constraint.subexpressions[1].name)
        # errors
        for error in constraint.errors:
            if error.is_indexed():
                assert_equals(result.json_errors['indexed_errors'][str(error.index)], error.error_message())
            else:
                assert error.error_message() in result.json_errors['unsorted_errors']