import math

class AiStatistics:

   def __init__(self, agent):

      self.agent = agent
      self.numSteps = 0

   def addStep(self):
      self.numSteps += 1

   def recordSample(self, plot):
      plot.addSample(self.numSteps)
      self.numSteps = 0


