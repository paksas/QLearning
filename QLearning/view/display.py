import sys
import pygame

class Display:

   def __init__(self):

      pygame.init()

      size = width, height = 640, 480
      self.black = 0, 0, 0

      self.screen = pygame.display.set_mode(size)
      self.font = pygame.font.SysFont("monospace", 15)

      self.keypressListener = None

   def renderBegin(self):

      self.screen.fill(self.black)
      return self.screen

   def renderEnd(self):
      pygame.display.flip()

   def buildLabel(self, msg, width = 1, color = (255, 255, 255)):
      label = self.font.render(msg, width, color)
      return label
      
   def handleEvents(self):

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            return False

         if event.type == pygame.KEYDOWN:
            self.__onKeyPress__()
        
      return True

   def setKeypressListener(self, listener):
      self.keypressListener = listener

   def __onKeyPress__(self):
      if self.keypressListener is not None:
         self.keypressListener()
