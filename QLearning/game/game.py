import view
import world
import utils
import ai
import numpy as np

class Game:

   def __init__(self):
      self.__initDisplay__()
      self.__initWorld__()
      self.__initKeyboardControls__()
      self.__initUtils__()
      self.__initAI__()

   def __initDisplay__(self):
      self.display = view.Display()

      self.gameModeLabel = [
         self.display.buildLabel("off-line"),
         self.display.buildLabel("training"),
         self.display.buildLabel("testing")]

   def __initWorld__(self):     
      self.resources = {
         '_': view.Resource('resources/grass.png'),
         '#': view.Resource('resources/wall.png'),
         'e': view.Resource('resources/cheese.png'),
         '@': view.Resource('resources/mouse.png')}

      self.scene = world.World(cellSize = np.array([32, 32]), resources = self.resources)

   def __initKeyboardControls__(self):
      self.display.setKeypressListener(lambda: self.__toggleNextMode__())

   def __initUtils__(self):
      self.timer = utils.Timer(0.001)
      self.efficiencyPlot = utils.EfficiencyPlot()

      self.timer.addToTick(lambda: self.__tick__())

   def __initAI__(self):
      self.gameMode = 0
      self.restartRequested = False
      self.mouse = None
      self.mouseAI = None
      self.cheese = None
      self.aiStatistics = None

   def loadMap(self, mapDefinitionStr):
      self.scene.loadLevel(mapDefinitionStr)

   def addMouse(self, pos):
      if self.mouse is not None:
         return self.mouseAI

      self.mouseStartPos = np.array(pos)
      self.mouse = world.Agent('@', self.mouseStartPos)
      self.scene.addAgent(self.mouse);
      self.timer.addToTick(lambda: self.mouseAI.think(self.scene))

      self.mouseAI = ai.MovingAI(agent = self.mouse, goalId = 'e', wallId = '#')
      self.mouseAI.setGoalReachedListener(lambda: self.__onGoalReached__())
      self.__onGameModeChanged__(self.gameMode, self.mouseAI, self.timer)

      self.aiStatistics = utils.AiStatistics(self.mouse)
      self.timer.addToTick(lambda: self.aiStatistics.addStep())

      return self.mouseAI

   def addCheese(self, pos):
      if self.cheese is not None:
         return self.cheese

      self.cheeseStartPos = np.array(pos)
      self.cheese = world.Agent('e', self.cheeseStartPos)
      self.scene.addAgent(self.cheese);

      return self.cheese

   def loop(self):
      while self.display.handleEvents():

         self.timer.tick()
      
         screen = self.display.renderBegin()
         self.scene.render(screen)
         screen.blit(self.gameModeLabel[self.gameMode], (500, 460))
         self.display.renderEnd()

   def __toggleNextMode__(self):
      self.gameMode = (self.gameMode + 1) % 3

      if self.mouseAI is not None:
         self.__onGameModeChanged__(self.gameMode, self.mouseAI, self.timer)

   def __onGameModeChanged__(self, gameMode, mouseAI, timer):

      if gameMode == 0:
         mouseAI.reset()
         timer.setPeriod(0.5)
      elif gameMode == 1:
         mouseAI.setLearningMode(True)
         timer.setPeriod(0.0001)
      elif gameMode == 2:
         mouseAI.setLearningMode(False)
         timer.setPeriod(0.5)

   def __requestRestart__(self):
      self.restartRequested = True

   def __resetScene__(self):
      if self.mouse is not None:
         self.mouse.setPos(self.mouseStartPos)

      if self.cheese is not None:
         self.cheese.setPos(self.cheeseStartPos)

   def __onGoalReached__(self):
      self.__resetScene__()
      self.aiStatistics.recordSample(self.efficiencyPlot)

   def __tick__(self):
      if self.restartRequested:
         self.restartRequested = False
         self.__resetScene__()

