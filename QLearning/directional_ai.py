import view
import world
import utils
import ai
import numpy as np

mapStr = \
   '____________________\n'\
   '____________________\n'\
   '____#_______________\n'\
   '____###_____________\n'\
   '____________________\n'\
   '____________________\n'\
   '____________________\n'\
   '____________________\n'\
   '____________________\n'\
   '____________________\n'\
   '____________________\n'\
   '____________________\n'\
   '____________________';

class DirectionalMouseAI(ai.MovingAI):

   def __init__(self, agent, cheese):

      ai.MovingAI.__init__(self, agent)
      
      self.cheese = cheese
      self.goalReachedListener = None

   def calculateReward(self, scene):

      reward = -1

      if (self.agent.getPos() == self.cheese.getPos()).all():
         reward = 50
         self.onGoalReached()

      return reward

   def calculateState(self, scene):
      dirToCheese = np.sign(self.cheese.getPos() - self.agent.getPos())

      for state in range(len(self.directions)):
         if (self.directions[state] == dirToCheese).all():
            return state

      return None


   def setGoalReachedListener(self, listener):
      self.goalReachedListener = listener

   def onGoalReached(self):
      if self.goalReachedListener is not None:
         self.goalReachedListener()


class GameController:

   def __init__(self, scene, efficiencyPlot, timer):

      self.scene = scene
      self.efficiencyPlot = efficiencyPlot
      self.timer = timer

      self.gameMode = 0

      self.cheese = world.Agent('e', scene.pickRandomLocation())
      self.mouse = world.Agent('@', scene.pickRandomLocation())
      scene.addAgent(self.mouse);
      scene.addAgent(self.cheese);

      self.aiStatistics = utils.AiStatistics(self.mouse, self.cheese)
      self.mouseAI = DirectionalMouseAI(self.mouse, self.cheese)  

      self.mouseAI.setGoalReachedListener(lambda: self.cheeseEaten())

      self.__onGameModeUpdated__()
      
   def addToTick(self, timer):
      timer.addToTick(lambda: self.mouseAI.think(scene))
      timer.addToTick(lambda: self.aiStatistics.addStep())

   def toggleNextMode(self):
      self.gameMode = (self.gameMode + 1) % 3
      self.__onGameModeUpdated__()

   def __onGameModeUpdated__(self):
      if self.gameMode == 0:
         self.mouseAI.reset()
         self.timer.setPeriod(0.5)
      elif self.gameMode == 1:
         self.mouseAI.setLearningMode()
         self.timer.setPeriod(0.0001)
      elif self.gameMode == 2:
         self.mouseAI.setTrainingMode()
         self.timer.setPeriod(0.5)

   def getGameMode(self):
      return self.gameMode

   def cheeseEaten(self):
      self.cheese.setPos(self.scene.pickRandomLocation())
      self.aiStatistics.recordSample(self.efficiencyPlot)


if __name__ == '__main__':
   
   display = view.Display()

   gameModeLabel = [
      display.buildLabel("off-line"),
      display.buildLabel("training"),
      display.buildLabel("testing")]

   resources = {
      ' ': view.Resource('resources/grass.png'),
      '#': view.Resource('resources/wall.png'),
      'e': view.Resource('resources/cheese.png'),
      '@': view.Resource('resources/mouse.png')}

   scene = world.World(cellSize = np.array([32, 32]), resources = resources)
   scene.loadLevel(mapStr)

   timer = utils.Timer(0.001)
   efficiencyPlot = utils.EfficiencyPlot()
   
   gameController = GameController(scene, efficiencyPlot, timer)
   gameController.addToTick(timer)

   display.setKeypressListener(lambda: gameController.toggleNextMode())

   while display.handleEvents():

      timer.tick()
      
      screen = display.renderBegin()
      scene.render(screen)
      screen.blit(gameModeLabel[gameController.getGameMode()], (500, 460))
      display.renderEnd()
