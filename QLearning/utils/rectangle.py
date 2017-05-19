import numpy as np

class Rectangle:
   
   def __init__(self, halfWidth, halfHeight):            
      self.pattern = []

      for y in range(-halfHeight, halfHeight + 1):
         for x in range(-halfWidth, halfWidth + 1):
            self.pattern.append(np.array([x, y]))

   def toWorldSpace(self, origin):
      worldSpacePattern = []
      for offset in self.pattern:
         worldSpacePattern.append(offset + origin)
   
      return worldSpacePattern

