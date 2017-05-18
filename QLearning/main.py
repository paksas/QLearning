import game
import ai

mapStr = \
   '#############\n'\
   '#     #     #\n'\
   '#           #\n'\
   '#############';

      
if __name__ == '__main__':
   
   game = game.Game()
   
   game.loadMap(mapStr)
   cheese = game.addCheese([8, 1])
   mouseAi = game.addMouse([1, 1])
  
   mouseAi.addSense(ai.Smell(cheese.getId()))
   mouseAi.addSense(ai.Eyesight(1))

   game.loop()


