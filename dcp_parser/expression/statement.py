import abc

class Statement(object):
    """ Abstract base class for Expression and Constraint """
    __metaclass__ = abc.ABCMeta
    # Takes short_name (string representation without subexpressions), subexpressions,
    # errors, and the parent expression.
    def __init__(self, short_name, subexpressions, errors = [], parent = None):
        self.short_name = short_name
        self.subexpressions = subexpressions
        self.init_subexpressions()
        self.errors = errors
        self.parent = parent

    # Initializes parent attribute of subexpressions
    def init_subexpressions(self):
        for exp in self.subexpressions:
            exp.parent = self