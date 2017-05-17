import RL
import numpy as np

class MovingAI:

   def __init__(self, agent):

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

      self.ai = RL.QLearn(numActions=len(self.directions), alpha=0.1, gamma=0.9)
      self.prevState = None
      self.prevAction = None
      self.isLearning = False

   def reset(self):
      self.ai.reset()
      self.prevState = None
      self.prevAction = None
      self.isLearning = False

   def setLearningMode(self):
      self.isLearning = True

   def setTrainingMode(self):
      self.isLearning = False

   def goInDirection(self, directionIdx, scene):
      newPos = self.agent.getPos() + self.directions[directionIdx]
      validNewPos = scene.wrapCoordinates(newPos)
      self.agent.setPos(validNewPos)

   def think(self, scene):
      currState = self.calculateState(scene)
      reward = self.calculateReward(scene)
      
      if self.isLearning:
         if self.prevState is not None:
            self.ai.learn(self.prevState, self.prevAction, currState, reward)

         action = self.ai.chooseAction(currState, epsilon = 0.1)
      else:
         action = self.ai.chooseAction(currState, epsilon = 0.0)
      
      self.prevState = currState
      self.prevAction = action

      self.goInDirection(action, scene)

   def calculateState(self, scene):
      return 0

   def calculateReward(self, scene):
      return -1
