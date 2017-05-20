import view
import world
import utils
import ai
import RL
import numpy as np
import pygame

class Game:

   def __init__(self):
      self.__initDisplay__()
      self.__initKeyboardControls__()
      self.__initWorld__()
      self.__initUI__()
      self.__initAI__()

   def __initDisplay__(self):
      self.display = view.Display()

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

   def __initAI__(self):    
      self.efficiencyPlot = view.Plot()

      self.aiCollection = ai.AICollection()
      self.positionMonitors = []
      self.trainedAI = ai.TrainedAI(goalId = 'e', wallId = '#', statisticsPlot = self.efficiencyPlot)      

      self.eyesight = ai.Eyesight(1)
      self.smell = ai.Smell('e')

      self.memory = RL.QMemory()
      self.savedMemory = None
      self.savedMemoryNo = -1
      
      self.timer = utils.Timer(0.5)
      self.efficiencyPlot.show()

      def updatePositionMonitors():
         for monitor in self.positionMonitors:
            monitor.update(self.scene)

      self.timer.addToTick(lambda: self.aiCollection.think(self.scene))
      self.timer.addToTick(updatePositionMonitors)

   def __initUI__(self):

      def onViewModeChanged(modeId):
         if modeId == 'player':          
            self.viewMode = self.__render_player_view__
         else:
            self.viewMode = self.__render_ai_view__

      def onBrainModeChanged(modeId):
         self.efficiencyPlot.resetPlot()
         if modeId == 'test':          
            self.timer.setPeriod(0.5)
            self.trainedAI.setLearningMode(False)
         else:
            self.timer.setPeriod(0.0001)
            self.efficiencyPlot.resetPlot()
            self.trainedAI.setLearningMode(True)
        
      def onEyesightChanged(modeId):
         if modeId == 'on':          
            self.aiCollection.addSense(self.eyesight)
         else:
            self.aiCollection.removeSense(self.eyesight)

      def onViewDistanceChanged(modeId):
         if modeId == 'near':          
            self.eyesight.setDistance(1)
         else:
            self.eyesight.setDistance(3)

      def onSmellChanged(modeId):
         if modeId == 'on':       
            self.aiCollection.addSense(self.smell)
         else:
            self.aiCollection.removeSense(self.smell)

      def onSave():
         self.savedMemoryNo += 1
         optionStr = 'save_{0}'.format(self.savedMemoryNo)
         self.uiOptions['save'].setOptions([optionStr])
         self.savedMemory = self.memory.save()

      def onLoad():
         self.uiOptions['memory'].setOption('test').execute()
         if self.savedMemory is not None:
            self.memory.load(self.savedMemory)        

      def onReset():
         self.efficiencyPlot.resetPlot()
         self.memory.clear()

      def onLoadMap(mapFilePath):
         mapDefinitionStr = self.__loadMapFile(mapFilePath)
         self.scene.loadLevel(mapStr = mapDefinitionStr, walkableCellId = '_')
         self.__buildAI__()
         self.uiOptions['eyesight'].execute()
         self.uiOptions['smell'].execute()

         
      self.ui = view.UI([440, 10])

      self.uiOptions = {}
      self.uiOptions['view'] = self.ui.addOption(
            key = 'F1', 
            label = 'view', 
            options = ['player', 'ai'], 
            action = lambda modeId: onViewModeChanged(modeId))

      self.uiOptions['memory'] = self.ui.addOption(
            key = 'F2', 
            label = 'memory', 
            options = ['test', 'learn'], 
            action = lambda modeId: onBrainModeChanged(modeId))

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
            options = ['on', 'off'], 
            action = lambda modeId: onEyesightChanged(modeId))

      self.uiOptions['smell'] = self.ui.addOption(
            key = 'F10', 
            label = 'smell', 
            options = ['on', 'off'], 
            action = lambda modeId: onSmellChanged(modeId))

      self.uiOptions['viewDist'] = self.ui.addOption(
            key = 'F11', 
            label = 'view dist.',
            options = ['near', 'far'],
            action = lambda modeId: onViewDistanceChanged(modeId))

      self.ui.addSeparator()

      self.uiOptions['map'] = self.ui.addOption( 
            key = '1-7', 
            label = 'maps',
            action = lambda optionId: onLoadMap(optionId))

      self.input.onKeyPressed(pygame.K_F1, lambda: self.uiOptions['view'].toggle().execute())
      self.input.onKeyPressed(pygame.K_F2, lambda: self.uiOptions['memory'].toggle().execute())
      self.input.onKeyPressed(pygame.K_F5, lambda: self.uiOptions['save'].execute())
      self.input.onKeyPressed(pygame.K_F6, lambda: self.uiOptions['load'].execute())
      self.input.onKeyPressed(pygame.K_F7, lambda: self.uiOptions['reset'].execute())
      self.input.onKeyPressed(pygame.K_F9, lambda: self.uiOptions['eyesight'].toggle().execute())
      self.input.onKeyPressed(pygame.K_F10, lambda: self.uiOptions['smell'].toggle().execute())
      self.input.onKeyPressed(pygame.K_F11, lambda: self.uiOptions['viewDist'].toggle().execute())
      
      self.input.onKeyPressed(pygame.K_1, lambda: self.uiOptions['map'].execute('resources/right_corridor.txt'))
      self.input.onKeyPressed(pygame.K_2, lambda: self.uiOptions['map'].execute('resources/left_corridor.txt'))
      self.input.onKeyPressed(pygame.K_3, lambda: self.uiOptions['map'].execute('resources/down_corridor.txt'))
      self.input.onKeyPressed(pygame.K_4, lambda: self.uiOptions['map'].execute('resources/up_corridor.txt'))
      self.input.onKeyPressed(pygame.K_5, lambda: self.uiOptions['map'].execute('resources/twisted_corridor.txt'))
      self.input.onKeyPressed(pygame.K_6, lambda: self.uiOptions['map'].execute('resources/maze_1.txt'))
      self.input.onKeyPressed(pygame.K_7, lambda: self.uiOptions['map'].execute('resources/maze_2.txt'))
         
   def loop(self):
      while self.shouldKeepRunning:

         self.input.handleEvents()
         self.timer.tick()
      
         screen = self.display.renderBegin()
         self.__render__(screen)
         self.display.renderEnd()

   def __loadMapFile(self, filePath):
      with open(filePath) as f:
         content = f.read()
         return content

   def __buildAI__(self):
      self.efficiencyPlot.resetPlot()
      self.aiCollection.clear()
      self.positionMonitors = []
      self.trainedAI.setAI(None)

      miceAgents = self.scene.collectAgents('@')
      for mouse in miceAgents:
         mouseAI = ai.MovingAI(agent = mouse, memory = self.memory)
         self.positionMonitors.append(ai.PositionMonitor(agent = mouse, goalId = 'e', teleportPos = mouse.getPos()))
         self.aiCollection.add(mouseAI)

      if self.aiCollection.len() > 0:
         self.trainedAI.setAI(self.aiCollection.getAI(0))

   def __render__(self, screen):
      self.viewMode(screen)
      self.ui.render(screen)

   def __render_player_view__(self, screen):

      self.worldRenderer.clear()
      
      self.scene.forEachCell(lambda cell: self.worldRenderer.renderCell(cell))

      self.worldRenderer.present(screen)

   def __render_ai_view__(self, screen):

      def __render_cell__(pos):
         correspondingCell = self.scene.getCellAtPos(pos)
         self.worldRenderer.renderCell(correspondingCell)

      self.worldRenderer.clear()
      
      self.aiCollection.forEachSense(lambda sense: sense.forEachScannedPos(lambda pos: __render_cell__(pos) ) )

      self.worldRenderer.present(screen)
