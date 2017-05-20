class PositionMonitor:

   def __init__(self, agent, goalId, teleportPos):

      self.agent = agent
      self.goalId = goalId
      self.teleportPos = teleportPos

   def update(self, scene):

      if self.goalId in scene.getAgentsIds(self.agent.getPos()):
         self.agent.setPos(self.teleportPos)
