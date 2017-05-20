import RL
import numpy as np
import random

class TrainedAI:

   def __init__(self, goalId, wallId, statisticsPlot):

      self.ai = None
      self.goalId = goalId
      self.wallId = wallId
      self.statisticsPlot = statisticsPlot

      self.prevState = None
      self.isLearning = False

      self.numSteps = 0

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

   def setLearningMode(self, enable):
      self.isLearning = enable

   def isActive(self):
      return self.isLearning

   def chooseAction(self, scene, agent, brain, newState, prevAction):
      
      self.numSteps += 1

      if self.prevState is not None:
         reward, goalReached = self.__calculateReward__(scene, agent)
         brain.learn(self.prevState, prevAction, newState, reward)

         if goalReached:
            self.__finishEpoch__()

      self.prevState = newState

      if random.random() < 0.3:
         newAction = brain.chooseRandomAction()
      else:
         newAction = brain.chooseAction(newState)
      
      return newAction

   def __calculateReward__(self, scene, agent):
      
      agentPos = agent.getPos()
      agentIds = scene.getAgentsIds(agentPos)
      goalReached = False

      if self.goalId in agentIds:
         reward = self.rewardEatCheese
         goalReached = True
      elif self.wallId in agentIds:
         reward = self.rewardCollision
      else:
         reward = self.rewardNothing

      return reward, goalReached

   def __finishEpoch__(self):
      self.statisticsPlot.addSample(self.numSteps)
      self.numSteps = 0