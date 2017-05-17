import random

class QLearn:

   def __init__(self, numActions, alpha=0.1, gamma=0.9):

      self.q = {}

      self.actions = range(numActions)
      self.alpha = alpha
      self.gamma = gamma

   def reset(self):
      self.q = {}

   def learn(self, prevState, prevAction, newState, reward):

      maxqnew = max([self.__getQ__(newState, a) for a in self.actions])
      self.__learnQ__(prevState, prevAction, reward, reward + self.gamma*maxqnew)

   def chooseAction(self, state, epsilon):

      if random.random() < epsilon:
         action = random.choice(self.actions)
         return action

      q = [self.__getQ__(state, a) for a in self.actions]
      maxQ = max(q)
      count = q.count(maxQ)
      if count > 1:
            best = [i for i in range(len(self.actions)) if q[i] == maxQ]
            i = random.choice(best)
      else:
            i = q.index(maxQ)

      action = self.actions[i]
      return action

   def __getQ__(self, state, action):
      return self.q.get((state, action), 0.0)

   def __learnQ__(self, state, action, reward, value):
      oldv = self.q.get((state, action), None)
      if oldv is None:
         self.q[(state, action)] = reward
      else:
         self.q[(state, action)] = oldv + self.alpha * (value - oldv)
