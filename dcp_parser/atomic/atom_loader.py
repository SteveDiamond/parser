from dcp_parser.expression.expression import Expression
from atoms import Atom
from dcp_parser.error_messages.dcp_violation_factory import DCPViolationFactory
# Methods to create a dict of atomic functions

# For a given atomic class creates a function that takes in arguments,
# passes them to the class constructor, and returns an Expression
# based on the class sign and curvature.
def make_atomic_func(atomic_class):
    def atomic_func(*args):
        instance = atomic_class(*args)
        func_name = instance.name()
        name = func_name + "("
        for i in range(len(args)):
            name += str(args[i])
            if i < len(args)-1: 
                name += ", " 
        name += ")"

        errors = DCPViolationFactory.composition_error(instance.signed_curvature(), 
                                                instance.monotonicity(),
                                                instance.argument_curvatures(),
                                                instance.argument_signs())
        return Expression(instance.curvature(), instance.sign(), name, instance.arguments(), 
                          errors = errors, 
                          monotonicity = instance.monotonicity(), 
                          short_name = instance.short_name())
    return atomic_func

# Creates a dict mapping atomic function names to generated atomic functions.
def generate_atom_dict():
    atom_dict = {}
    for subclass in get_subclasses(Atom):
        name = subclass.__name__.lower()
        func = make_atomic_func(subclass)
        atom_dict[name] = func
    return atom_dict

# Returns a list of all classes derived at some point from the given class.
def get_subclasses(cls):
    subcls = []
    if hasattr(cls, '__subclasses__'):
        subcls = cls.__subclasses__()
        for cls in subcls:
            subcls = subcls + get_subclasses(cls)
    return subcls