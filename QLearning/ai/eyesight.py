import utils
from functools import reduce

class Eyesight:

   def __init__(self, range):
      self.sensesPattern = utils.Rectangle(range, range)
      self.idToPriorityMap = {
         '_' : 0,
         '@' : 1,
         '#' : 2,
         'e' : 3
      }

   def scan(self, scene, agentPos):
      pattern = self.sensesPattern.toWorldSpace(agentPos)
      
      stateVec = []
      for pos in pattern:
         dynamicIds = scene.getAgentsIds(pos)

         selectedState = reduce((lambda x,y: max(x, y)), map(lambda id: self.idToPriorityMap[id], dynamicIds))
         stateVec.append(selectedState)

      return stateVec     
            



