import utils

class Smell:

   def __init__(self, smelledAgentId):
      self.smelledAgentId = smelledAgentId

   def scan(self, scene, agentPos):

      smelledAgents = filter(lambda agent: agent.getId() == self.smelledAgentId, scene.getAgents())

      stateVec = []
      for smelledAgent in smelledAgents:
         stateVec.append(utils.calculateDirectionIndex(smelledAgent.getPos(), agentPos))

      return stateVec
