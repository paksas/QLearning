import numpy as np
import random
import itertools


def getValidTransitions(x): 

   validTransitionsFlags = map(lambda x: x >= 0, x)
   validTranistionsIndices = itertools.compress(np.arange(len(x)), validTransitionsFlags)

   return list(validTranistionsIndices)

def simulateEpisode(Q, R, gamma, goalState):

   print('simulateEpisode start')

   numStates, numActions = R.shape
   print('numStates = {0}, numActions = {1}'.format(numStates, numActions))

   initialState = random.randint(0, numStates - 1)
   
   state = initialState
   while state != goalState:

      print('-------------')
      print('entering state = ', state)

      actionCosts = R[state, :]
      print('actionCosts = ', actionCosts)

      availableTransitions = getValidTransitions(actionCosts)
      print('availableTransitions = ', availableTransitions)

      actionIdx = random.randint(0, len(availableTransitions) - 1)
      action = availableTransitions[actionIdx]

      print('selected action = ', action )

      nextState = action # ???

      availableTransitionsInNextState = getValidTransitions(R[nextState, :])

      availableActionsCosts = Q[nextState][availableTransitionsInNextState]
      print('Q costs of available actions = ', availableActionsCosts)

      bestActionIdx = np.argmax(availableActionsCosts)
      print('best action idx = ', bestActionIdx)

      qCost = R[state][action] + gamma * availableActionsCosts[bestActionIdx]
      print('qCost of [{0}][{1}] = {2}'.format(nextState, action, qCost))

      Q[state][action] += qCost

      state = action


   Qflat = Q.flatten()
   maxVal = Qflat[np.argmax(Qflat)]

   Q = Q / maxVal

def main():

   mtxQ = np.zeros((6, 6))

   mtxR = np.array([
      [-1, -1, -1, -1,  0,  -1],
      [-1, -1, -1,  0, -1, 1],
      [-1, -1, -1,  0, -1,  -1],
      [-1,  0,  0, -1,  0,  -1],
      [ 0, -1, -1,  0, -1, 1],
      [-1,  0, -1, -1,  0, 1]
      ])

   gamma = 0.8

   for i in np.arange(100):
      simulateEpisode(mtxQ, mtxR, gamma, 5)

   print('mtxQ = ', mtxQ)

if __name__ == '__main__':
   main()
