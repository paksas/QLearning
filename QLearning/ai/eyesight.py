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

      self.seenPositions = []

   def setDistance(self, range):
      self.sensesPattern = utils.Rectangle(range, range)

   def forEachScannedPos(self, cb):
      for pos in self.seenPositions:
         cb(pos)

   def scan(self, scene, agentPos):
      self.seenPositions = self.sensesPattern.toWorldSpace(agentPos)
      
      stateVec = []
      for pos in self.seenPositions:
         dynamicIds = scene.getAgentsIds(pos)
         if len(dynamicIds) > 0:
            selectedState = reduce((lambda x,y: max(x, y)), map(lambda id: self.idToPriorityMap[id], dynamicIds))
            stateVec.append(selectedState)

      return stateVec     
            