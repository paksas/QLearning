import math

class AiStatistics:

   def __init__(self):

      self.isActive = False
      self.numSteps = 0

   def setActive(self, enable):
      self.isActive = enable

   def addStep(self):
      if self.isActive:
         self.numSteps += 1

   def recordSample(self, plot):
      if self.isActive:
         plot.addSample(self.numSteps)
         self.numSteps = 0


