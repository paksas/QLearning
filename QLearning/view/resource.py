import pygame

class Resource:

   def __init__(self, fileName):

      self.sprite = pygame.image.load(fileName)
      self.rect = self.sprite.get_rect()

   def getSize(self):
      return [self.rect.width, self.rect.height]

   def render(self, screen, pos):

      renderRect = self.rect.move(pos)
      screen.blit(self.sprite, renderRect)
