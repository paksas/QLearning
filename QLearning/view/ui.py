from .resource import Resource
import numpy as np
import pygame

class UIEntry:

   def __init__(self, menu, position, key, label, action):

      self.menu = menu
      self.position = position

      self.keyLabel = self.menu.valueFont.render(key, 1, (255, 255, 255))
      self.labelLabel = self.menu.labelFont.render(label, 1, (255, 255, 255))
      self.optionLabels = []
      self.options = []
      self.action = action
      self.activeOptionIdx = -1

   def render(self, screen):
      screen.blit(self.keyLabel, (self.position[0], self.position[1]))
      screen.blit(self.labelLabel, (self.position[0] + 30, self.position[1]))

      if self.activeOptionIdx >= 0:
         screen.blit(self.optionLabels[self.activeOptionIdx], (self.position[0] + 110, self.position[1]))

   def setOptions(self, options):

      self.optionLabels = []
      for option in options:
         self.optionLabels.append(self.menu.valueFont.render(option.upper(), 1, (255, 255, 255)))
      self.options = options

      if len(self.optionLabels) > 0:
         self.activeOptionIdx = 0
      else:
         self.activeOptionIdx = -1

      return self

   def toggle(self):
      if self.activeOptionIdx >= 0:
         self.activeOptionIdx = (self.activeOptionIdx + 1) % len(self.options)

      return self

   def setOption(self, option):

      idx = self.options.index(option)
      if idx >= 0:
         self.activeOptionIdx = idx

      return self

   def execute(self):
      option = None
      if self.activeOptionIdx >= 0:
         option = self.options[self.activeOptionIdx]

      self.action(option)
      return self

class UIMultichoiceEntry:

   def __init__(self, menu, position, label, numOptions, action):
      self.menu = menu
      self.position = position

      self.labelLabel = self.menu.labelFont.render(label, 1, (255, 255, 255))
      optionLabelStr = str([optionIdx + 1 for optionIdx in range(numOptions)])
      self.optionLabel = self.menu.valueFont.render(optionLabelStr, 1, (255, 255, 255))

      self.action = action

   def render(self, screen):
      screen.blit(self.labelLabel, (self.position[0], self.position[1]))
      screen.blit(self.optionLabel, (self.position[0], self.position[1] + 20))

   def execute(self, value):
      self.action(value)
      return self

class UI:

   def __init__(self, topLeft):

      self.nextEntryPos = np.array(topLeft)
      self.entriesSpacing = np.array([0, 32])
      self.entries = []

      self.labelFont = pygame.font.SysFont("monospace", 14)
      self.valueFont = pygame.font.SysFont("monospace", 14)
      self.valueFont.set_bold(True)


   def addOption(self, key, label, options = [], action = None):

      entryPos = self.nextEntryPos
      self.nextEntryPos = self.nextEntryPos + self.entriesSpacing

      entry = UIEntry(self, entryPos, key, label, action)
      entry.setOptions(options)
      self.entries.append(entry)
      return entry

   def addMultichoiceOption(self, label, numOptions, action = None):

      entryPos = self.nextEntryPos
      self.nextEntryPos = self.nextEntryPos + self.entriesSpacing

      entry = UIMultichoiceEntry(self, entryPos, label, numOptions, action)
      self.entries.append(entry)
      return entry

   def addSeparator(self):
      self.nextEntryPos = self.nextEntryPos + self.entriesSpacing

   def render(self, screen):

      for entry in self.entries:
         entry.render(screen)

