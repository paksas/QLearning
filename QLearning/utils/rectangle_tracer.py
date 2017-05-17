import numpy as np 


class RectangleTracer:

   def __init__(self):

      self.firstBlockOffset = [
         np.array([ 0, -1]),
         np.array([ 1,  0]),
         np.array([ 0,  1]),
         np.array([-1,  0]) ];

      self.sideDir = [
         np.array([ 1,  0]),
         np.array([ 0,  1]),
         np.array([-1,  0]),
         np.array([ 0, -1]) ];

      pass

   def trace(self, sideLen, cellIndex):
      
      sideIdx = cellIndex % sideLen
      blockIdx = cellIndex - sideIdx * sideLen
      halfSideLen = sideLen / 2

      firstBlockOffset = np.round(( self.firstBlockOffset[sideIdx] - self.sideDir[sideIdx] ) * halfSideLen)
      blockCoord = firstBlockOffset + self.sideDir[sideIdx] * blockIdx

      nextCellIdx = cellIndex + 1
      numCellsInCircumference = (sideLen - 1) * 4
      newSideLen = sideLen
      if (nextCellIdx > numCellsInCircumference):
         nextCellIdx = 0
         newSideLen += 1

      return blockCoord, nextCellIdx, newSideLen


