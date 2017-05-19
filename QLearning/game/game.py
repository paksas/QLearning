import view
import world
import utils
import ai
import numpy as np
import pygame

class Game:

   def __init__(self):
      self.__initDisplay__()
      self.__initKeyboardControls__()
      self.__initUI__()
      self.__initWorld__()
      self.__initUtils__()
      self.__initAI__()

   def __initDisplay__(self):
      self.display = view.Display()

      self.gameModeLabel = [
         self.display.buildLabel("off-line"),
         self.display.buildLabel("training"),
         self.display.buildLabel("testing")]

      self.viewMode = self.__render_player_view__

   def __initWorld__(self):     
      self.resources = {
         '_': view.Resource('resources/grass.png'),
         '#': view.Resource('resources/wall.png'),
         'e': view.Resource('resources/cheese.png'),
         '@': view.Resource('resources/mouse.png')}

      self.scene = world.World()

      self.worldRenderer = world.WorldRenderer(
         resources = self.resources, 
         cellSize = np.array([32, 32]) )

   def __initKeyboardControls__(self):
      self.input = view.Input()
      self.shouldKeepRunning = True

      def toggleKeepRunning():
         self.shouldKeepRunning = False

      self.input.onQuit(lambda: toggleKeepRunning())

   def __initUtils__(self):
      self.timer = utils.Timer(0.001)
      self.efficiencyPlot = utils.EfficiencyPlot()

   def __initAI__(self):
      self.gameMode = 0
      self.mouse = None
      self.mouseAI = None
      self.cheese = None
      self.aiStatistics = None

   def __initUI__(self):

      self.ui = view.UI()
      self.ui.registerInputHandlers(self.input)

      self.viewModes = {
         'player' : self.__render_player_view__,
         'ai' : self.__render_ai_view__ }

      self.gameModes = {
         'off-line' : 0,
         'learn' : 1,
         'test' : 2}

      def onViewModeChanged(modeId):
         self.viewMode = self.viewModes[modeId]

      def onMemoryModeChanged(modeId):
         self.gameMode = self.gameModes[modeId]         
         if self.mouseAI is not None:
            self.__onGameModeChanged__(self.gameMode, self.mouseAI, self.timer)

      def onEyesightChanged(modeId):
         pass

      def onSmellChanged(modeId):
         pass

      def onSave():
         pass

      def onLoad():
         pass

      def onSetMap(mapId):
         pass

      self.ui.onViewModeChanged(lambda modeId: onViewModeChanged(modeId))
      self.ui.onMemoryModeChanged(lambda modeId: onMemoryModeChanged(modeId))
      self.ui.onEyesightChanged(lambda modeId: onEyesightChanged(modeId))
      self.ui.onSmellChanged(lambda modeId: onSmellChanged(modeId))
      self.ui.onSave(lambda: onSave())
      self.ui.onLoad(lambda: onLoad())
      self.ui.onSetMap(lambda: onSetMap(mapId))

   def loadMap(self, mapDefinitionStr):
      self.scene.loadLevel(mapStr = mapDefinitionStr, walkableCellId = '_')

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

      while self.shouldKeepRunning:

         self.input.handleEvents()
         self.timer.tick()
      
         screen = self.display.renderBegin()
         self.__render__(screen)
         screen.blit(self.gameModeLabel[self.gameMode], (500, 460))
         self.display.renderEnd()

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

   def __resetScene__(self):
      if self.mouse is not None:
         self.mouse.setPos(self.mouseStartPos)

      if self.cheese is not None:
         self.cheese.setPos(self.cheeseStartPos)

   def __onGoalReached__(self):
      self.__resetScene__()
      self.aiStatistics.recordSample(self.efficiencyPlot)

   def __render__(self, screen):
      self.viewMode(screen)
      self.ui.render(screen)

   def __render_player_view__(self, screen):

      self.worldRenderer.clear()
      
      self.scene.forEachCell(lambda cell: self.worldRenderer.renderCell(cell))

      self.worldRenderer.present(screen)

   def __render_ai_view__(self, screen):

      if self.mouse is None:
         return

      def __render_cell__(pos):
         correspondingCell = self.scene.getCellAtPos(pos)
         self.worldRenderer.renderCell(correspondingCell)

      self.worldRenderer.clear()
      
      __render_cell__(self.mouse.getPos())
      self.mouseAI.forEachSense(lambda sense: sense.forEachScannedPos(lambda pos: __render_cell__(pos) ) )

      self.worldRenderer.present(screen)
