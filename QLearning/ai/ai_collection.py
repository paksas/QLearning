class AICollection:

   def __init__(self):
      self.collection = []

   def add(self, ai, agent):
      self.collection.append((ai, agent, agent.getPos()))

   def clear(self):
      self.collection = []

   def len(self):
      return len(self.collection)

   def getAI(self, idx):
      ai, agent, pos = self.collection[idx]
      return ai

   def getAgent(self, idx):
      ai, agent, pos = self.collection[idx]
      return agent

   def addSense(self, sense):
      for ai, agent, pos in self.collection:
         ai.addSense(sense)

   def removeSense(self, sense):
      for ai, agent, pos in self.collection:
         ai.removeSense(sense)

   def forEachSense(self, cb):
      for ai, agent, pos in self.collection:
         ai.forEachSense(cb)

   def resetPositions(self):
      for ai, agent, pos in self.collection:
         agent.setPos(pos)

   def think(self, scene):
      for ai, agent, pos in self.collection:
         ai.think(scene)

