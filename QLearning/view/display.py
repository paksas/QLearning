import sys
import pygame

class Display:

   def __init__(self):

      pygame.init()

      size = width, height = 640, 480
      self.black = 0, 0, 0

      self.screen = pygame.display.set_mode(size)

   def renderBegin(self):

      self.screen.fill(self.black)
      return self.screen

   def renderEnd(self):
      pygame.display.flip()
       
   def keepRunning(self):

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
           return False
        
      return True

