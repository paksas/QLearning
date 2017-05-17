import view
import world
import utils
import agents
import numpy as np

mapStr = \
   '          \n'\
   '          \n'\
   '          \n'\
   '          \n'\
   '          \n'\
   '          ';


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
   
   aiStatistics = utils.AiStatistics(mouse, cheese)

   mouseAI = agents.MouseAI(mouse, cheese)  
   mouseAI.setGoalReachedListener(lambda: aiStatistics.recordSample(efficiencyPlot))
 
   timer.addToTick(lambda: mouseAI.think(scene))
   timer.addToTick(lambda: aiStatistics.addStep())

   while display.keepRunning():

      timer.tick()
      
      screen = display.renderBegin()
      scene.render(screen)
      display.renderEnd()
