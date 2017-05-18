import io
import random
import utils
import numpy as np 
from .agent import Agent

class World:

   def __init__(self):

      self.unoccupiedSpaceTracer = utils.RectangleTracer()

   def loadLevel(self, mapStr, walkableCellId = '_'):

      buf = io.StringIO(mapStr)
      lines = buf.readlines()

      numLines = len(lines)
      lineWidth = len(lines[0]) - 1

      self.worldShape = np.array([lineWidth, numLines])
      self.cells = [
         [WorldCell(np.array([x, y]), walkableCellId) 
          for y in range(self.worldShape[1])] 
            for x in range(self.worldShape[0])]
      self.agents = []
      
      for y in range(self.worldShape[1]):

         parsedLine = lines[y]
         totalLineLen = len(parsedLine)
         parsedLineLen = min(totalLineLen, self.worldShape[0])
         for x in range(parsedLineLen):

            resourceId = parsedLine[x]
            if resourceId != '' and resourceId != ' ' and resourceId != '\n':
               agent = Agent(resourceId, np.array([x, y]))
               self.cells[x][y].addAgent(agent)

      return self

   def forEachCell(self, cb):
      for col in self.cells:
         for cell in col:
            cb(cell)

   def getCellAtPos(self, localPos):
      return self.cells[localPos[0]][localPos[1]]

   def addAgent(self, agent):

      self.agents.append(agent)
      agent.setWorld(self)

      agentPos = agent.getPos()
      cell = self.cells[agentPos[0]][agentPos[1]]
      cell.addAgent(agent)

      return self

   def getAgents(self):
      return self.agents

   def moveAgent(self, agent, prevPos, newPos):
         prevCell = self.cells[prevPos[0]][prevPos[1]]
         newCell = self.cells[newPos[0]][newPos[1]]

         prevCell.removeAgent(agent)
         newCell.addAgent(agent)

   def getAgentsIds(self, localPos):
      validPos = self.wrapCoordinates(localPos)
      cell = self.cells[validPos[0]][validPos[1]]

      agentIds = []
      cell.forEachAgent(lambda agent: agentIds.append(agent.getId()))
      
      return agentIds

   def isPositionOccupied(self, localPos):
      validPos = self.wrapCoordinates(localPos)
      return cell.hasAnyAgents()

   def findClosestUnoccupiedPosition(self, localPos):

      testedCoords = localPos
      cellIdx = 0
      sideLen = 3
      while self.isPositionOccupied(testedCoords):

         sideLen, cellIdx, blockCoord = self.unoccupiedSpaceTracer.trace(sideLen, cellIdx)
         testedCoords = self.wrapCoordinates(blockCoord + localPos)

      return testedCoords

   def wrapCoordinates(self, localPos):

      validLocalPos = np.array(localPos)

      while(validLocalPos[0] < 0):
         validLocalPos[0] += self.worldShape[0]

      while(validLocalPos[1] < 0):
         validLocalPos[1] += self.worldShape[1]

      validLocalPos = validLocalPos % self.worldShape

      return validLocalPos

   def pickRandomLocation(self):

      origin = np.array([
         random.randint(0, self.worldShape[0] - 1), 
         random.randint(0, self.worldShape[1] - 1)])

      validPos = self.findClosestUnoccupiedPosition(origin)
      return validPos

class WorldCell:

   def __init__(self, localPos, backgroundId):
      self.localPos = localPos
      self.backgroundId = backgroundId
      self.agents = []

   def getPos(self):
      return self.localPos

   def getBgResourceId(self):
      return self.backgroundId

   def addAgent(self, agent):
      self.agents.append(agent)

   def removeAgent(self, agent):
      self.agents.remove(agent)

   def forEachAgent(self, cb):
      for agent in self.agents:
         cb(agent)

   def hasAnyAgents(self):
      return len(self.agents) > 0


class WorldRenderer:

   def __init__(self, resources, cellSize):
      self.resources = resources
      self.cellSize = cellSize
      self.cells = []

   def clear(self):
      self.cells = []

   def renderCell(self, cell):
      self.cells.append(cell)

   def present(self, screen):

      def __render__(resourceId, worldPos):
         resource = self.resources[resourceId]
         if resource is not None:
            resource.render(screen, worldPos)

      for cell in self.cells:
         worldPos = cell.getPos() * self.cellSize
         __render__(cell.getBgResourceId(), worldPos)

         cell.forEachAgent(lambda agent: __render__(agent.getId(), worldPos))

