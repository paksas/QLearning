import sys
import pygame

class Display:

   def __init__(self):

      pygame.init()

      size = width, height = 640, 480
      self.black = 0, 0, 0

      self.screen = pygame.display.set_mode(size)
      self.font = pygame.font.SysFont("monospace", 15)

   def renderBegin(self):

      self.screen.fill(self.black)
      return self.screen

   def renderEnd(self):
      pygame.display.flip()

   def buildLabel(self, msg, width = 1, color = (255, 255, 255)):
      label = self.font.render(msg, width, color)
      return label
      
