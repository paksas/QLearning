import time

class Timer:

   def __init__(self, period):
      self.prevTime = time.time()
      self.elapsedTime = 0
      self.period = period
      
      self.totalTimeElapsed = 0

      self.callbacks = []

   def setPeriod(self, period):
      self.period = period

   def getTimeElapsed(self):
      return self.totalTimeElapsed

   def tick(self):

      currTime = time.time()

      elapsedTime = currTime - self.prevTime
      self.elapsedTime += elapsedTime
      self.totalTimeElapsed += elapsedTime

      self.prevTime = currTime

      if self.elapsedTime >= self.period:
         self.elapsedTime = 0
         
         self.__invokeCallbacks__()

   def addToTick(self, callback):
      self.callbacks.append(callback)

   def __invokeCallbacks__(self):
      for cb in self.callbacks:
         cb()