import view
import world
import utils
import agents
import numpy as np

mapStr = \
   '                    \n'\
   '                    \n'\
   '    #               \n'\
   '    ###             \n'\
   '                    \n'\
   '                    \n'\
   '                    \n'\
   '                    \n'\
   '                    \n'\
   '                    \n'\
   '                    \n'\
   '                    \n'\
   '                    ';

class GameController:

   def __init__(self, mouseAI):
      self.gameMode = 0
      self.mouseAI = mouseAI

   def toggleNextMode(self):
      self.gameMode = (self.gameMode + 1) % 3

      if self.gameMode == 0:
         self.mouseAI.reset()
      elif self.gameMode == 1:
         self.mouseAI.setLearningMode()
      elif self.gameMode == 2:
         self.mouseAI.setTrainingMode()

   def getGameMode(self):
      return self.gameMode

if __name__ == '__main__':
   
   display = view.Display()

   gameModeLabel = [
      display.buildLabel("off-line"),
      display.buildLabel("training"),
      display.buildLabel("testing")]

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
   
   aiStatistics = utils.AiStatistics(mouse, cheese)

   mouseAI = agents.MouseAI(mouse, cheese)  
   mouseAI.setGoalReachedListener(lambda: aiStatistics.recordSample(efficiencyPlot))
 
   timer.addToTick(lambda: mouseAI.think(scene))
   timer.addToTick(lambda: aiStatistics.addStep())

   gameController = GameController(mouseAI)
   display.setKeypressListener(lambda: gameController.toggleNextMode())

   while display.handleEvents():

      timer.tick()
      
      screen = display.renderBegin()
      scene.render(screen)
      screen.blit(gameModeLabel[gameController.getGameMode()], (500, 460))
      display.renderEnd()
