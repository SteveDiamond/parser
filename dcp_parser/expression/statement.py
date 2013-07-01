import abc

class Statement(object):
    """ Abstract base class for Expression and Constraint """
    __metaclass__ = abc.ABCMeta
    # Takes short_name (string representation without subexpressions), 
    # subexpressions, and errors.
    def __init__(self, short_name, subexpressions, errors = []):
        self.short_name = short_name
        self.subexpressions = subexpressions
        self.errors = errors