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
      self.timer = utils.Timer(0.5)
      self.efficiencyPlot = utils.EfficiencyPlot()

   def __initAI__(self):
      self.gameMode = 0
      self.mouse = None
      self.mouseAI = None
      self.eyesight = ai.Eyesight(1)
      self.smell = ai.Smell('e')
      self.cheese = None
      self.aiStatistics = None

   def __initUI__(self):

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
         if modeId == 'on':          
            self.mouseAI.addSense(self.eyesight)
         else:
            self.mouseAI.removeSense(self.eyesight)

      def onViewDistanceChanged(modeId):
         if modeId == 'near':          
            self.eyesight.setDistance(1)
         else:
            self.eyesight.setDistance(3)


      def onSmellChanged(modeId):
         if modeId == 'on':       
            self.mouseAI.addSense(self.smell)
         else:
            self.mouseAI.removeSense(self.smell)

      def onSave():
         pass

      def onLoad():
         pass

      def onTimeMultiplierChanged(modeId):
         if modeId == 'normal':
            self.timer.setPeriod(0.5)
         else:
            self.timer.setPeriod(0.0001)

      def onSetMap(mapId):
         pass

      self.ui = view.UI([440, 10])

      viewModeOpt = self.ui.addOption(
            key = 'F1', 
            label = 'view', 
            options = ['player', 'ai'], 
            action = lambda modeId: onViewModeChanged(modeId))

      memoryModeOpt = self.ui.addOption(
            key = 'F2', 
            label = 'memory', 
            options = ['off-line', 'learn', 'test'], 
            action = lambda modeId: onMemoryModeChanged(modeId))

      timeMulToggleOpt = self.ui.addOption(
            key = 'F3', 
            label = 'time',
            options = ['normal', 'fast'],
            action = lambda modeId: onTimeMultiplierChanged(modeId))

      self.ui.addSeparator()

      saveOpt = self.ui.addOption(
            key = 'F5', 
            label = 'save',
            action = lambda: onSave())

      loadOpt = self.ui.addOption(
            key = 'F6', 
            label = 'load',
            action = lambda: onLoad())

      self.ui.addSeparator()

      eyesightToggleOpt = self.ui.addOption(
            key = 'F9', 
            label = 'eyes', 
            options = ['off', 'on'], 
            action = lambda modeId: onEyesightChanged(modeId))

      smellToggleOpt = self.ui.addOption(
            key = 'F10', 
            label = 'smell', 
            options = ['off', 'on'], 
            action = lambda modeId: onSmellChanged(modeId))

      viewDistanceToggleOpt = self.ui.addOption(
            key = 'F11', 
            label = 'view dist',
            options = ['near', 'far'],
            action = lambda modeId: onViewDistanceChanged(modeId))

      self.input.onKeyPressed(pygame.K_F1, viewModeOpt.execute)
      self.input.onKeyPressed(pygame.K_F2, memoryModeOpt.execute)
      self.input.onKeyPressed(pygame.K_F3, timeMulToggleOpt.execute)
      self.input.onKeyPressed(pygame.K_F5, saveOpt.execute)
      self.input.onKeyPressed(pygame.K_F6, loadOpt.execute)
      self.input.onKeyPressed(pygame.K_F9, eyesightToggleOpt.execute)
      self.input.onKeyPressed(pygame.K_F10, smellToggleOpt.execute)
      self.input.onKeyPressed(pygame.K_F11, viewDistanceToggleOpt.execute)
         

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
      elif gameMode == 1:
         mouseAI.setLearningMode(True)
      elif gameMode == 2:
         mouseAI.setLearningMode(False)

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
      
      self.mouseAI.forEachSense(lambda sense: sense.forEachScannedPos(lambda pos: __render_cell__(pos) ) )

      self.worldRenderer.present(screen)
