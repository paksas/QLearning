import view
import world
import utils
import RL
import random
import math
import numpy as np

mapStr = \
   '          \n'\
   '          \n'\
   '          \n'\
   '          \n'\
   '          \n'\
   '          ';

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

   def getSuccessRate(self):
      return 2.0

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

class LogicLoop:

   def __init__(self, mouseAI, aiStatistics):
      self.mouseAI = mouseAI
      self.aiStatistics = aiStatistics

   def tick(self):
      self.mouseAI.think(scene)
      self.aiStatistics.addStep()

if __name__ == '__main__':
   
   display = view.Display()

   resources = {
      ' ': view.Resource('resources/ground.png'),
      '#': view.Resource('resources/wall.png'),
      'e': view.Resource('resources/finish.png'),
      '@': view.Resource('resources/mouse.png')}

   scene = world.World(cellSize = np.array([32, 32]), resources = resources)
   scene.loadLevel(mapStr)

   cheese = world.Agent('e', scene.pickRandomLocation())
   mouse = world.Agent('@', scene.pickRandomLocation())
   scene.addAgent(mouse);
   scene.addAgent(cheese);
  
   timer = utils.Timer(0.001)
   efficiencyPlot = utils.EfficiencyPlot()
   
   aiStatistics = AiStatistics(mouse, cheese)

   mouseAI = MouseAI(mouse, cheese)  
   mouseAI.setGoalReachedListener(lambda: aiStatistics.recordSample(efficiencyPlot))

   logicLoop = LogicLoop(mouseAI, aiStatistics)

   while display.keepRunning():

      timer.tick(lambda: logicLoop.tick())
      
      if ( aiStatistics.getSuccessRate() <= 1.5 ):
         timer.setPeriod(0.5)

      screen = display.renderBegin()
      scene.render(screen)
      display.renderEnd()
