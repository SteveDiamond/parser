from sign import Sign

class Vexity:
  """ Vexity for a convex optimization expression. """
  CONSTANT_KEY = 'CONSTANT'
  AFFINE_KEY = 'AFFINE'
  CONVEX_KEY = 'CONVEX'
  CONCAVE_KEY = 'CONCAVE'
  NONCONVEX_KEY = 'NONCONVEX'
  
  """
  VEXITY_MAP for resolving vexity addition using bitwise OR:
    CONSTANT (0) | ANYTHING = ANYTHING
    AFFINE (1) | NONCONSTANT = NONCONSTANT
    CONVEX (3) | CONCAVE (5) = NONCONVEX (7)
    SAME | SAME = SAME
  """
  VEXITY_MAP = {
                CONSTANT_KEY: 0,
                AFFINE_KEY: 1, 
                CONVEX_KEY: 3, 
                CONCAVE_KEY: 5,
                NONCONVEX_KEY: 7
               }

  # For multiplying vexity by negative sign.
  NEGATION_MAP = {CONVEX_KEY: CONCAVE_KEY, CONCAVE_KEY: CONVEX_KEY}
  # For multiplying vexity by unknown sign.
  UNKNOWN_MAP = {CONVEX_KEY: NONCONVEX_KEY, CONCAVE_KEY: NONCONVEX_KEY}
  
  def __init__(self,vexity_str):
      if vexity_str in Vexity.VEXITY_MAP.keys():
          self.vexity_str = vexity_str
      else:
          raise Exception("No such vexity %s exists." % str(vexity_str))
      
  def __repr__(self):
      return "Vexity('%s')" % self.vexity_str
  
  def __str__(self):
      return self.vexity_str
      
  def __add__(self, other):
      vexity_val = Vexity.VEXITY_MAP[self.vexity_str] | Vexity.VEXITY_MAP[other.vexity_str]
      for key,val in Vexity.VEXITY_MAP.items():
          if val == vexity_val:
              return Vexity(key)
  
  def __sub__(self, other):
      return self + -other

  # Captures interaction of constant sign and vexity
  def sign_mult(self, sign):
      if sign == Sign(Sign.UNKNOWN_KEY):
          vexity_str = Vexity.UNKNOWN_MAP.get(self.vexity_str, self.vexity_str)
          return Vexity(vexity_str)
      elif sign == Sign(Sign.ZERO_KEY):
          return Vexity(Vexity.CONSTANT_KEY)
      elif sign == Sign(Sign.NEGATIVE_KEY):
          vexity_str = Vexity.NEGATION_MAP.get(self.vexity_str, self.vexity_str)
          return Vexity(vexity_str)
      else: # Positive sign
          return self
     
  def __mul__(self, other):
      if self == Vexity(Vexity.CONSTANT_KEY) or other == Vexity(Vexity.CONSTANT_KEY):
          return self + other
      else:
          return Vexity(Vexity.NONCONVEX_KEY)

  def __div__(self, other):
      if other == Vexity(Vexity.CONSTANT_KEY):
          return self + other
      else:
          return Vexity(Vexity.NONCONVEX_KEY)
      
  def __neg__(self):
      return self.sign_mult(Sign(Sign.NEGATIVE_KEY))
      
  def __eq__(self,other):
      return self.vexity_str == other.vexity_str
  
  def __ne__(self,other):
      return self.vexity_str != other.vexity_str