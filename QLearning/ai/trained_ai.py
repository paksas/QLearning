import RL
import numpy as np
import random

class TrainedAI:

   def __init__(self, goalId, wallId):

      self.ai = None
      self.goalId = goalId
      self.wallId = wallId

      self.prevState = None
      self.isLearning = False

      self.goalReachedListener = None

      self.setRewards()
      
   def setAI(self, ai):
      if self.ai is not None:
         self.ai.installLearningModule(None)

      self.ai = ai

      if self.ai is not None:
         self.ai.installLearningModule(self)

   def setRewards(self, eatingCheese=50, collision =-25, nothing = -1):
      self.rewardEatCheese = eatingCheese
      self.rewardCollision = collision
      self.rewardNothing = nothing

   def setGoalReachedListener(self, listener):
      self.goalReachedListener = listener

   def setLearningMode(self, enable):
      self.isLearning = enable

   def isActive(self):
      return self.isLearning

   def chooseAction(self, scene, agent, brain, newState, prevAction):
      
      if self.prevState is not None:
         reward = self.__calculateReward__(scene, agent)
         brain.learn(self.prevState, prevAction, newState, reward)

      self.prevState = newState

      if random.random() < 0.1:
         newAction = brain.chooseRandomAction()
      else:
         newAction = brain.chooseAction(newState)
      
      return newAction

   def __calculateReward__(self, scene, agent):
      
      agentPos = agent.getPos()
      agentIds = scene.getAgentsIds(agentPos)

      if self.goalId in agentIds:
         reward = self.rewardEatCheese
         self.__onGoalReached__()
      elif self.wallId in agentIds:
         reward = self.rewardCollision
      else:
         reward = self.rewardNothing

      return reward

   def __onGoalReached__(self):
      if self.goalReachedListener is not None:
         self.goalReachedListener()
