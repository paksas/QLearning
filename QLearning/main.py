import game
import ai

mapStr = \
   '#############\n'\
   '#@    #    e#\n'\
   '#           #\n'\
   '#############';

      
if __name__ == '__main__':
   
   game = game.Game()
   
   game.loadMap(mapStr)

   game.loop()


