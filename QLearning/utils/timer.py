import time

class Timer:

   def __init__(self, period):
      self.prevTime = time.time()
      self.elapsedTime = 0
      self.period = period
      
      self.totalTimeElapsed = 0

   def setPeriod(self, period):
      self.period = period

   def getTimeElapsed(self):
      return self.totalTimeElapsed

   def tick(self, callback):

      currTime = time.time()

      elapsedTime = currTime - self.prevTime
      self.elapsedTime += elapsedTime
      self.totalTimeElapsed += elapsedTime

      self.prevTime = currTime

      if self.elapsedTime >= self.period:
         self.elapsedTime = 0
         callback()

