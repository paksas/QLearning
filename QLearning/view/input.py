import sys
import pygame

class Input:

   def __init__(self):
      self.keypressListeners = {}
      self.quitHandler = None

   def handleEvents(self):

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            if self.quitHandler is not None:
               self.quitHandler()

         if event.type == pygame.KEYDOWN:
            keyHandler = self.keypressListeners.get(event.key)
            if keyHandler is not None:
               keyHandler()
        
      return True

   def onQuit(self, listener):
      self.quitHandler = listener

   def onKeyPressed(self, keyCode, listener):
      self.keypressListeners[keyCode] = listener

