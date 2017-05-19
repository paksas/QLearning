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
      self.savedBrain = None
      self.savedBrainNo = -1

   def __initUI__(self):

      def onViewModeChanged(modeId):
         if modeId == 'player':          
            self.viewMode = self.__render_player_view__
         else:
            self.viewMode = self.__render_ai_view__

      def onBrainModeChanged(modeId):
         if modeId == 'test':          
            self.mouseAI.setLearningMode(False)
         else:
            self.mouseAI.setLearningMode(True)
        
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
         self.savedBrainNo += 1
         optionStr = 'save_{0}'.format(self.savedBrainNo)
         self.uiOptions['save'].setOptions([optionStr])
         self.savedBrain = self.mouseAI.save()

      def onLoad():
         self.uiOptions['brain'].setOption('test').execute()
         if self.savedBrain is not None:
            self.mouseAI.load(self.savedBrain)          

      def onReset():
         self.uiOptions['brain'].setOption('test').execute()
         self.mouseAI.reset()

      def onTimeMultiplierChanged(modeId):
         if modeId == 'normal':
            self.timer.setPeriod(0.5)
         else:
            self.timer.setPeriod(0.0001)

      def onSetMap(mapId):
         pass

      self.ui = view.UI([440, 10])

      self.uiOptions = {}
      self.uiOptions['view'] = self.ui.addOption(
            key = 'F1', 
            label = 'view', 
            options = ['player', 'ai'], 
            action = lambda modeId: onViewModeChanged(modeId))

      self.uiOptions['brain'] = self.ui.addOption(
            key = 'F2', 
            label = 'brain', 
            options = ['test', 'learn'], 
            action = lambda modeId: onBrainModeChanged(modeId))

      self.uiOptions['time'] = self.ui.addOption(
            key = 'F3', 
            label = 'time',
            options = ['normal', 'fast'],
            action = lambda modeId: onTimeMultiplierChanged(modeId))

      self.ui.addSeparator()

      self.uiOptions['save'] = self.ui.addOption(
            key = 'F5', 
            label = 'save',
            action = lambda _: onSave())

      self.uiOptions['load'] = self.ui.addOption(
            key = 'F6', 
            label = 'load',
            action = lambda _: onLoad())

      self.uiOptions['reset'] = self.ui.addOption(
            key = 'F7', 
            label = 'reset',
            action = lambda _: onReset())


      self.ui.addSeparator()

      self.uiOptions['eyesight'] = self.ui.addOption(
            key = 'F9', 
            label = 'eyes', 
            options = ['off', 'on'], 
            action = lambda modeId: onEyesightChanged(modeId))

      self.uiOptions['smell'] = self.ui.addOption(
            key = 'F10', 
            label = 'smell', 
            options = ['off', 'on'], 
            action = lambda modeId: onSmellChanged(modeId))

      self.uiOptions['viewDist'] = self.ui.addOption(
            key = 'F11', 
            label = 'view dist.',
            options = ['near', 'far'],
            action = lambda modeId: onViewDistanceChanged(modeId))

      self.input.onKeyPressed(pygame.K_F1, lambda: self.uiOptions['view'].toggle().execute())
      self.input.onKeyPressed(pygame.K_F2, lambda: self.uiOptions['brain'].toggle().execute())
      self.input.onKeyPressed(pygame.K_F3, lambda: self.uiOptions['time'].toggle().execute())
      self.input.onKeyPressed(pygame.K_F5, lambda: self.uiOptions['save'].execute())
      self.input.onKeyPressed(pygame.K_F6, lambda: self.uiOptions['load'].execute())
      self.input.onKeyPressed(pygame.K_F7, lambda: self.uiOptions['reset'].execute())
      self.input.onKeyPressed(pygame.K_F9, lambda: self.uiOptions['eyesight'].toggle().execute())
      self.input.onKeyPressed(pygame.K_F10, lambda: self.uiOptions['smell'].toggle().execute())
      self.input.onKeyPressed(pygame.K_F11, lambda: self.uiOptions['viewDist'].toggle().execute())
         
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
      self.mouseAI.setLearningMode(False)

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
