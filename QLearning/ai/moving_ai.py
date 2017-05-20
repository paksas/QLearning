import RL
import numpy as np

class MovingAI:

   def __init__(self, agent, memory):

      self.agent = agent

      self.directions = [
         np.array([1, -1]), 
         np.array([1, 0]),
         np.array([1, 1]),
         np.array([-1, -1]), 
         np.array([-1, 0]),
         np.array([-1, 1]),
         np.array([0, -1]), 
         np.array([0, 0]),
         np.array([0, 1])]

      self.senses = []

      self.brain = RL.QLearn(numActions = len(self.directions), memory = memory)
      self.scheduledAction = None
      self.learningModule = None
      
   def installLearningModule(self, module):
      self.learningModule = module

   def addSense(self, sense):
      self.senses.append(sense)

   def removeSense(self, sense):
      self.senses.remove(sense)

   def forEachSense(self, cb):
      for sense in self.senses:
         cb(sense)

   def think(self, scene):

      if self.scheduledAction is not None:
         self.__goInDirection__(self.scheduledAction, scene)

      state = self.__calculateState__(scene)

      if self.learningModule is not None and self.learningModule.isActive():
         self.scheduledAction = self.learningModule.chooseAction(scene, self.agent, self.brain, state, self.scheduledAction)
      else:
         self.scheduledAction = self.brain.chooseAction(state)      

   def __calculateState__(self, scene):
      agentPos = self.agent.getPos()

      state = []
      for sense in self.senses:
         senseResult = sense.scan(scene, agentPos)
         state += senseResult

      return tuple(state)

   def __goInDirection__(self, directionIdx, scene):
      newPos = self.agent.getPos() + self.directions[directionIdx]
      validNewPos = scene.wrapCoordinates(newPos)
      self.agent.setPos(validNewPos)
