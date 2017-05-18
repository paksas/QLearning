class Agent:

   def __init__(self, id, pos):
      self.id = id
      self.pos = pos
      self.world = None

   def getPos(self):
      return self.pos

   def setPos(self, newPos):
      if self.world is not None:
         self.world.moveAgent(self, self.pos, newPos)

      self.pos = newPos

   def getId(self):
      return self.id

   def setWorld(self, world):
      self.world = world
