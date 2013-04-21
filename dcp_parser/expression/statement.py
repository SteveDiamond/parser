import abc

class Statement(object):
    """ Abstract base class for Expression and Constraint """
    __metaclass__ = abc.ABCMeta
    def __init__(self, subexpressions, errors = [], parent = None):
        self.subexpressions = subexpressions
        self.init_subexpressions()
        self.errors = errors

    # Initializes parent attribute of subexpressions
    def init_subexpressions(self):
        for exp in self.subexpressions:
            exp.parent = self