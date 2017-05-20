class AICollection:

   def __init__(self):
      self.collection = []
      self.positionMonitors = []

   def add(self, ai):
      self.collection.append(ai)

   def clear(self):
      self.collection = []

   def len(self):
      return len(self.collection)

   def getAI(self, idx):
      ai = self.collection[idx]
      return ai

   def addSense(self, sense):
      for ai in self.collection:
         ai.addSense(sense)

   def removeSense(self, sense):
      for ai in self.collection:
         ai.removeSense(sense)

   def forEachSense(self, cb):
      for ai in self.collection:
         ai.forEachSense(cb)

   def think(self, scene):
      for ai in self.collection:
         ai.think(scene)

