from dcp_parser.atomic.atoms import *
from dcp_parser.atomic.atom_loader import *
from dcp_parser.expression.expression import *
from nose.tools import *

class TestAtomLoader(object):
    """ Unit tests for the atomic/atom_loader module. """
    @classmethod
    def setup_class(self):
        self.cvx_pos = Expression(Curvature.CONVEX, Sign.POSITIVE, 'cvx_pos')

    # Test creation of functions from atom classes.
    def test_make_atomic_func(self):
        square = make_atomic_func(Square)
        exp = square(self.cvx_pos)
        assert_equals(exp.curvature, Curvature.CONVEX)
        assert_equals(str(exp), 'square(cvx_pos)')

        max = make_atomic_func(Max)
        exp = max(self.cvx_pos, Variable('x'), Constant(-1))
        assert_equals(exp.curvature, Curvature.CONVEX)
        assert_equals(str(exp), 'max(cvx_pos, x, -1)')

    # Test creation of atom dict
    def test_generate_atom_dict(self):
        atom_dict = generate_atom_dict()
        assert_equals(len(atom_dict), len(get_subclasses(Atom)))
        assert('square' in atom_dict)