class Sign(object):
    """ Sign of convex optimization expressions. """
    POSITIVE_KEY = 'POSITIVE'
    NEGATIVE_KEY = 'NEGATIVE'
    UNKNOWN_KEY = 'UNKNOWN'
    ZERO_KEY = 'ZERO'
    
    # SIGN_MAP for resolving sign addition using bitwise OR
    SIGN_MAP = {ZERO_KEY: 0, POSITIVE_KEY: 1, NEGATIVE_KEY: 2, UNKNOWN_KEY: 3}
    
    def __init__(self,sign_str):
        if sign_str in Sign.SIGN_MAP.keys():
            self.sign_str = sign_str
        else:
            raise Exception("No such sign %s exists." % str(sign_str))

    # Returns whether the sign string is a valid sign type.
    @staticmethod
    def is_sign(sign_str):
        return sign_str in Sign.SIGN_MAP.keys()

        
    def __add__(self, other):
        sign_val = Sign.SIGN_MAP[self.sign_str] | Sign.SIGN_MAP[other.sign_str]
        for key,val in Sign.SIGN_MAP.items():
            if val == sign_val:
                return Sign(key)
    
    def __sub__(self, other):
        return self + -other
       
    def __mul__(self, other):
        if self == Sign(Sign.ZERO_KEY) or other == Sign(Sign.ZERO_KEY):
            return Sign(Sign.ZERO_KEY)
        elif self == Sign(Sign.UNKNOWN_KEY) or other == Sign(Sign.UNKNOWN_KEY):
            return Sign(Sign.UNKNOWN_KEY)
        elif self != other:
            return Sign(Sign.NEGATIVE_KEY)
        else:
            return Sign(Sign.POSITIVE_KEY)

    def __div__(self, other):
        if other == Sign(Sign.ZERO_KEY):
            raise Exception("Divide by zero error.")
        else:
            return self * other
        
    def __neg__(self):
        return self * Sign(Sign.NEGATIVE_KEY)
        
    def __eq__(self,other):
        return self.sign_str == other.sign_str
    
    def __ne__(self,other):
        return self.sign_str != other.sign_str

    def __repr__(self):
        return "Sign('%s')" % self.sign_str
    
    def __str__(self):
        return self.sign_str