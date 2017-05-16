import view
import world
import utils
import RL
import random
import matplotlib.pyplot as plt
import math
import numpy as np

mapStr = \
   '          \n'\
   '          \n'\
   '          \n'\
   '          \n'\
   '          \n'\
   '          ';


class MouseAI:

   def __init__(self, agent, cheese):
      self.agent = agent
      self.cheese = cheese

      self.numSuccesses = 0

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

      self.ai = RL.QLearn(numActions=len(self.directions), alpha=0.1, gamma=0.9, epsilon = 0.1)
      self.prevState = None
      self.prevAction = None

   def think(self, scene):

      currState = self.calcState()
      reward = -1

      if (self.agent.getPos() == self.cheese.getPos()).all():
         reward = 50
         self.numSuccesses += 1
         self.cheese.setPos(scene.pickRandomLocation())

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

   def getNumSuccesses(self):
     return self.numSuccesses


class EfficiencyPlot:

   def __init__(self):

      self.nextIdx = 0

      self.ydata = []
      plt.show()

      self.axes = plt.gca()
      self.axes.set_xlim(0, 100)
      self.axes.set_ylim(-50, +50)

      self.line, = self.axes.plot(self.ydata, 'r-')

   def addSample(self, val):

      self.xdata.append(self.nextIdx)
      self.nextIdx += 1

      self.ydata.append(val)

      self.line.set_xdata(self.xdata)
      self.line.set_ydata(self.ydata)
      plt.draw()

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

   simulationdDelay = 0.001
   timer = utils.Timer(simulationdDelay)
   mouseAI = MouseAI(mouse, cheese)  

   # efficiencyPlot = EfficiencyPlot()

   while display.keepRunning():

      timer.tick(lambda: mouseAI.think(scene))
      
      # efficiencyPlot.addSample(mouseAI.getEfficiencyChange())
      if ( mouseAI.getNumSuccesses() > 1000 ):
         timer.setPeriod(0.5)

      screen = display.renderBegin()
      scene.render(screen)
      display.renderEnd()
