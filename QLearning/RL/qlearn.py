import random

class QLearn:

   def __init__(self, numActions, memory):

      self.memory = memory

      self.actions = range(numActions)

   def learn(self, prevState, prevAction, newState, reward, alpha=0.1, gamma=0.9):

      maxqnew = max([self.memory.get(newState, a) for a in self.actions])
      self.memory.learn(prevState, prevAction, reward, reward + gamma*maxqnew, alpha)

   def chooseRandomAction(self):
      action = random.choice(self.actions)
      return action

   def chooseAction(self, state):

      q = [self.memory.get(state, a) for a in self.actions]
      maxQ = max(q)
      count = q.count(maxQ)
      if count > 1:
            best = [i for i in range(len(self.actions)) if q[i] == maxQ]
            i = random.choice(best)
      else:
            i = q.index(maxQ)

      action = self.actions[i]
      return action
