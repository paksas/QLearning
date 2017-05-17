import view
import world
import utils
import ai
import numpy as np

mapStr = \
   '#############\n'\
   '#_____#_____#\n'\
   '#___________#\n'\
   '#############';


class MouseWithSensesAI(ai.MovingAI):

   def __init__(self, agent):
      ai.MovingAI.__init__(self, agent)
      
      self.eyesight = ai.Eyesight(1)
      self.smell = ai.Smell('e')
      self.goalReachedListener = None

   def calculateReward(self, scene):
      
      agentPos = self.agent.getPos()
      if 'e' in scene.getAgentsIds(agentPos):
         reward = 50
         self.onGoalReached()
      elif scene.getStaticId(agentPos) == '#':
         reward = -25
      else:
         reward = -1

      return reward

   def calculateState(self, scene):
      agentPos = self.agent.getPos()

      eyesightState = self.eyesight.scan(scene, agentPos)
      smellState = self.smell.scan(scene, agentPos)

      return tuple(eyesightState + smellState)

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
      self.restartRequested = False

      self.mouseStartPos = np.array([1, 1])
      self.cheeseStartPos = np.array([8, 1])

      self.cheese = world.Agent('e', self.cheeseStartPos)
      self.mouse = world.Agent('@', self.mouseStartPos)
      scene.addAgent(self.mouse);
      scene.addAgent(self.cheese);

      self.aiStatistics = utils.AiStatistics(self.mouse, self.cheese)
      self.mouseAI = MouseWithSensesAI(self.mouse)  

      self.mouseAI.setGoalReachedListener(lambda: self.requestRestart())

      self.__onGameModeUpdated__()
      
   def addToTick(self, timer):
      timer.addToTick(lambda: self.mouseAI.think(scene))
      timer.addToTick(lambda: self.aiStatistics.addStep())
      timer.addToTick(lambda: self.tick())

   def toggleNextMode(self):
      self.gameMode = (self.gameMode + 1) % 3
      self.requestRestart()

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

   def requestRestart(self):
      self.restartRequested = True

   def restart(self):
      self.mouse.setPos(self.mouseStartPos)
      self.cheese.setPos(self.cheeseStartPos)
      self.aiStatistics.recordSample(self.efficiencyPlot)
      self.__onGameModeUpdated__()


   def tick(self):
      if self.restartRequested:
         self.restartRequested = False
         self.restart()

   def render(self, screen):
      self.mouseAI.render(screen)
      
if __name__ == '__main__':
   
   display = view.Display()

   gameModeLabel = [
      display.buildLabel("off-line"),
      display.buildLabel("training"),
      display.buildLabel("testing")]

   resources = {
      '_': view.Resource('resources/grass.png'),
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

