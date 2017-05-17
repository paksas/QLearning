import math

class AiStatistics:

   def __init__(self, agent, goal):

      self.agent = agent
      self.goal = goal

      self.__startRecording__()

   def addStep(self):
      self.numSteps += 1

   def recordSample(self, plot):

      if self.expectedNumSteps > 0.0:
         predictionAccuracy = self.numSteps / self.expectedNumSteps
         plot.addSample(predictionAccuracy)

      self.__startRecording__()

   def __startRecording__(self):
      self.numSteps = 0
      self.expectedNumSteps = self.__predictNumSteps__()

   def __predictNumSteps__(self):
      diff = self.agent.getPos() - self.goal.getPos()
      return math.fabs(diff[0]) + math.fabs(diff[1])

