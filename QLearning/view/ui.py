from .resource import Resource
import numpy as np
import pygame

class UIEntry:

   def __init__(self, position, keyLabel, labelLabel, optionLabels, options, action):

      self.position = position
      self.keyLabel = keyLabel
      self.labelLabel = labelLabel
      self.optionLabels = optionLabels
      self.options = options
      self.action = action

      if len(self.optionLabels) > 0:
         self.activeOptionIdx = 0
      else:
         self.activeOptionIdx = -1

   def render(self, screen):

      screen.blit(self.keyLabel, (self.position[0], self.position[1]))
      screen.blit(self.labelLabel, (self.position[0] + 30, self.position[1]))

      if self.activeOptionIdx >= 0:
         screen.blit(self.optionLabels[self.activeOptionIdx], (self.position[0] + 110, self.position[1]))

   def execute(self):
      if self.activeOptionIdx >= 0:

         self.activeOptionIdx = (self.activeOptionIdx + 1) % len(self.options)

         option = self.options[self.activeOptionIdx]

         self.action(option)

class UI:

   def __init__(self, topLeft):

      self.nextOptionPos = np.array(topLeft)
      self.optionsSpacing = np.array([0, 32])
      self.entries = []

      self.labelFont = pygame.font.SysFont("monospace", 14)
      self.valueFont = pygame.font.SysFont("monospace", 14)
      self.valueFont.set_bold(True)


   def addOption(self, key, label, options = [], action = None):

      keyLabel = self.valueFont.render(key, 1, (255, 255, 255))
      labelLabel = self.labelFont.render(label, 1, (255, 255, 255))

      optionLabels = []
      for option in options:
         optionLabels.append(self.valueFont.render(option.upper(), 1, (255, 255, 255)))

      optionPos = self.nextOptionPos
      self.nextOptionPos = self.nextOptionPos + self.optionsSpacing

      option = UIEntry(optionPos, keyLabel, labelLabel, optionLabels, options, action)
      self.entries.append(option)
      return option

   def addSeparator(self):
      self.nextOptionPos = self.nextOptionPos + self.optionsSpacing

   def render(self, screen):

      for entry in self.entries:
         entry.render(screen)

