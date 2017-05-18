import RL
import numpy as np

class MovingAI:

   def __init__(self, agent, goalId, wallId):

      self.agent = agent
      self.goalId = goalId
      self.wallId = wallId

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
      self.setRewards()

      self.ai = RL.QLearn(numActions=len(self.directions), alpha=0.1, gamma=0.9)
      self.prevState = None
      self.prevAction = None
      self.isLearning = False
      self.goalReachedListener = None
      
   def addSense(self, sense):
      self.senses.append(sense)

   def setRewards(self, eatingCheese=50, collision =-25, nothing = -1):
      self.rewardEatCheese = eatingCheese
      self.rewardCollision = collision
      self.rewardNothing = nothing

   def setGoalReachedListener(self, listener):
      self.goalReachedListener = listener

   def reset(self):
      self.ai.reset()
      self.prevState = None
      self.prevAction = None
      self.isLearning = False

   def setLearningMode(self, enable):
      self.isLearning = enable

   def think(self, scene):
      currState = self.__calculateState__(scene)
      reward = self.__calculateReward__(scene)
      
      if self.isLearning:
         if self.prevState is not None:
            self.ai.learn(self.prevState, self.prevAction, currState, reward)

         action = self.ai.chooseAction(currState, epsilon = 0.1)
      else:
         action = self.ai.chooseAction(currState, epsilon = 0.0)
      
      self.prevState = currState
      self.prevAction = action

      self.__goInDirection__(action, scene)

   def __calculateReward__(self, scene):
      
      agentPos = self.agent.getPos()
      if self.goalId in scene.getAgentsIds(agentPos):
         reward = self.rewardEatCheese
         self.__onGoalReached__()
      elif scene.getStaticId(agentPos) == self.wallId:
         reward = self.rewardCollision
      else:
         reward = self.rewardNothing

      return reward

   def __calculateState__(self, scene):
      agentPos = self.agent.getPos()

      state = []
      for sense in self.senses:
         senseResult = sense.scan(scene, agentPos)
         state += senseResult

      return tuple(state)

   def __onGoalReached__(self):
      if self.goalReachedListener is not None:
         self.goalReachedListener()

   def __goInDirection__(self, directionIdx, scene):
      newPos = self.agent.getPos() + self.directions[directionIdx]
      validNewPos = scene.wrapCoordinates(newPos)
      self.agent.setPos(validNewPos)
