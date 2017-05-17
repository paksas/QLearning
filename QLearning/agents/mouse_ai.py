import numpy as np
import RL

class MouseAI:

   def __init__(self, agent, cheese):

      self.agent = agent
      self.cheese = cheese

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

      self.goalReachedListener = None

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

   def think(self, scene):
      currState = self.calcState()
      reward = -1

      if (self.agent.getPos() == self.cheese.getPos()).all():
         reward = 50
         self.cheese.setPos(scene.pickRandomLocation())
         self.onGoalReached()

      if self.isLearning:
         if self.prevState is not None:
            self.ai.learn(self.prevState, self.prevAction, currState, reward)

         action = self.ai.chooseAction(currState, epsilon = 0.1)
      else:
         action = self.ai.chooseAction(currState, epsilon = 0.0)
      
      self.prevState = currState
      self.prevAction = action

      self.goInDirection(action, scene)

   def calcState(self):

      dirToCheese = np.sign(self.cheese.getPos() - self.agent.getPos())

      for state in range(len(self.directions)):
         if (self.directions[state] == dirToCheese).all():
            return state

      return None

   def goInDirection(self, directionIdx, scene):
         newPos = self.agent.getPos() + self.directions[directionIdx]
         validNewPos = scene.wrapCoordinates(newPos)
         if scene.isPositionOccupied(validNewPos) == False:
            self.agent.setPos(validNewPos)

   def setGoalReachedListener(self, listener):
      self.goalReachedListener = listener

   def onGoalReached(self):

      if self.goalReachedListener is not None:
         self.goalReachedListener()

