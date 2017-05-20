import copy

class QMemory:

   def __init__(self):
      self.memory = {}

   def get(self, state, action):
      return self.memory.get((state, action), 0.0)

   def learn(self, state, action, reward, value, alpha):
      oldv = self.memory.get((state, action), None)
      if oldv is None:
         self.memory[(state, action)] = reward
      else:
         self.memory[(state, action)] = oldv + alpha * (value - oldv)

   def save(self):
      return copy.deepcopy(self.memory)        

   def load(self, memoryDump):
      self.memory = copy.deepcopy(memoryDump)        

   def clear(self):
      self.memory = {}
