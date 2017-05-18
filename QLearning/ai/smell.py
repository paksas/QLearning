import utils

class Smell:

   def __init__(self, smelledAgentId):
      self.smelledAgentId = smelledAgentId
      self.smelledPositions = []

   def forEachScannedPos(self, cb):
      for pos in self.smelledPositions:
         cb(pos)

   def scan(self, scene, agentPos):

      smelledAgentsArr = filter(lambda agent: agent.getId() == self.smelledAgentId, scene.getAgents())
      self.smelledPositions = [agent.getPos() for agent in smelledAgentsArr]

      stateVec = []
      for pos in self.smelledPositions:
         stateVec.append(utils.calculateDirectionIndex(pos, agentPos))

      return stateVec
   