from dcp_parser.expression.expression import Expression
from atoms import Atom
# Methods to create a dict of atomic functions

# For a given atomic class creates a function that takes in arguments,
# passes them to the class constructor, and returns an Expression
# based on the class sign and curvature.
def make_atomic_func(atomic_class):
    def atomic_func(*args):
        instance = atomic_class(*args)
        func_name = atomic_class.__name__.lower()

        # Check that args is not empty
        args = list(args)
        if len(args) == 0:
            raise Exception('%s requires at least one argument.' % func_name)
        
        name = func_name + "(" + str(args[0])
        for i in range(1,len(args)):
            name += ", " + str(args[i])
        name += ")"
        return Expression(instance.curvature(), instance.sign(), name, args)
    return atomic_func

# Creates a dict mapping atomic function names to generated atomic functions.
def generate_atom_dict():
    atom_dict = {}
    for subclass in Atom.__subclasses__():
        name = subclass.__name__.lower()
        func = make_atomic_func(subclass)
        atom_dict[name] = func
    return atom_dict


