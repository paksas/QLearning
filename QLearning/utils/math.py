import numpy as np

def calculateDirectionIndex(dest, origin):
   signDiff = np.sign(dest - origin)
   directionIndex = (signDiff[1] + 1) * 3 + (signDiff[0] + 1)
   return directionIndex

