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

      self.ai = RL.QLearn(numActions=len(self.directions), alpha=0.1, gamma=0.9, epsilon = 0.1)
      self.prevState = None
      self.prevAction = None

   def think(self, scene):

      currState = self.calcState()
      reward = -1

      if (self.agent.getPos() == self.cheese.getPos()).all():
         reward = 50
         self.cheese.setPos(scene.pickRandomLocation())
         self.onGoalReached()

      if self.prevState is not None:
         self.ai.learn(self.prevState, self.prevAction, currState, reward)

      action = self.ai.chooseAction(currState)
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
         self.agent.setPos(validNewPos)

   def setGoalReachedListener(self, listener):
      self.goalReachedListener = listener

   def onGoalReached(self):

      if self.goalReachedListener is not None:
         self.goalReachedListener()

