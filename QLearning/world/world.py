import io
import random
import utils
import numpy as np 

class World:

   def __init__(self, cellSize, resources):

      self.cellSize = cellSize
      self.mappingsDict = resources

      self.unoccupiedSpaceTracer = utils.RectangleTracer()

      self.agents = []
      self.staticCellsPrecomputed = []

   def __calculateRenderable__(self, resourceId, localPos):

      worldPos = localPos * self.cellSize
      resource = self.mappingsDict[resourceId]
      return (resource, worldPos)

   def addAgent(self, agent):
      self.agents.append(agent)
      return self

   def loadLevel(self, mapStr):

      buf = io.StringIO(mapStr)
      lines = buf.readlines()

      worldShape = [len(lines[0]) - 1, len(lines)]
      self.staticCells = np.chararray(shape = worldShape)

      for y in range(len(lines)):

         parsedLine = lines[y]
         for x in range(len(parsedLine)):

            c = parsedLine[x]
            if ( c == '\n'):
               continue

            self.staticCells[x, y] = c
            self.staticCellsPrecomputed.append(self.__calculateRenderable__(c, [x, y]))

      return self

   def render(self, screen):

      for resource, worldPos in self.staticCellsPrecomputed:         
         resource.render(screen, worldPos)

      for agent in self.agents:       
         resource, worldPos = self.__calculateRenderable__(agent.getId(), agent.getPos())
         resource.render(screen, worldPos)

      return self

   def getStaticId(self, localPos):

      if (localPos[0] < 0 or localPos[1] < 0 or localPos[0] >= self.staticCells.shape[0] or localPos[1] >= self.staticCells.shape[1]):
         return None

      return self.staticCells[localPos[0], localPos[1]]

   def isPositionOccupied(self, localPos):
      return self.getStaticId(localPos) != ''

   def findClosestUnoccupiedPosition(self, localPos):

      testedCoords = localPos
      cellIdx = 0
      sideLen = 3
      while self.isPositionOccupied(testedCoords):

         blockCoord, sideLen, cellId = self.unoccupiedSpaceTracer.trace(sideLen, cellIdx)
         testedCoords = blockCoord + localPos

      return testedCoords

   def wrapCoordinates(self, localPos):

      validLocalPos = np.array(localPos)

      while(validLocalPos[0] < 0):
         validLocalPos[0] += self.staticCells.shape[0]

      while(validLocalPos[1] < 0):
         validLocalPos[1] += self.staticCells.shape[1]

      validLocalPos = validLocalPos % self.staticCells.shape

      return validLocalPos

   def pickRandomLocation(self):

      origin = np.array([
         random.randint(0, self.staticCells.shape[0] - 1), 
         random.randint(0, self.staticCells.shape[1] - 1)])

      validPos = self.findClosestUnoccupiedPosition(origin)
      return validPos
