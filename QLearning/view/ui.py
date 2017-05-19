from .resource import Resource
import numpy as np
import pygame

class UIEntry:

   def __init__(self, resources, label, values, pos):

      self.label = resources[label]

      self.values = []
      self.valuesStr = values
      for value in values:
         self.values.append(resources[value])

      self.labelPos = np.array(pos)
      self.valuePos = np.array(pos) + np.array([100, 0])

      if len(self.values) > 0:
         self.selectedValueIdx = 0
      else:
         self.selectedValueIdx = -1

   def render(self, screen):

      self.label.render(screen, self.labelPos)

      if self.selectedValueIdx >= 0:
         self.values[self.selectedValueIdx].render(screen, self.valuePos)

   def toggleNextValue(self):
      numValues = len(self.values)
      if numValues > 0:
         self.selectedValueIdx = (self.selectedValueIdx + 1) % numValues
         return self.valuesStr[self.selectedValueIdx]
      else:
         self.selectedValueIdx = -1
         return None

class UI:

   def __init__(self):

      self.resources = {
         'view': Resource('resources/label_view.png'),
         'memory': Resource('resources/label_memory.png'),
         'eyesight': Resource('resources/label_eyesight.png'),
         'smell': Resource('resources/label_smell.png'),
         'save': Resource('resources/label_save.png'),
         'load': Resource('resources/label_load.png'),
         'time': Resource('resources/label_time.png'),
         'map': Resource('resources/label_map.png'),
         'ai': Resource('resources/value_ai.png'),
         'learn': Resource('resources/value_learn.png'),
         'off': Resource('resources/value_off.png'),
         'off-line': Resource('resources/value_off_line.png'),
         'on': Resource('resources/value_on.png'),
         'player': Resource('resources/value_player.png'),
         'test': Resource('resources/value_test.png'),
         'normal': Resource('resources/value_normal.png'),
         'fast': Resource('resources/value_fast.png'),}

      vertOffset = 10
      horizOffset = 440
      self.entries = {
         'view': UIEntry(self.resources, 'view', ['player', 'ai'], [horizOffset, vertOffset]),
         'memory': UIEntry(self.resources, 'memory', ['off-line', 'learn', 'test'], [horizOffset, vertOffset + 32 * 1]),
         'eyesight': UIEntry(self.resources, 'eyesight', ['off', 'on'], [horizOffset, vertOffset + 32 * 2]),
         'smell': UIEntry(self.resources, 'smell', ['off', 'on'], [horizOffset, vertOffset + 32 * 3]),
         'save': UIEntry(self.resources, 'save', [], [horizOffset, vertOffset + 32 * 4]),
         'load': UIEntry(self.resources, 'load', [], [horizOffset, vertOffset + 32 * 5]),
         'time': UIEntry(self.resources, 'time', ['normal', 'fast'], [horizOffset, vertOffset + 32 * 6]),
         'map': UIEntry(self.resources, 'map', [], [horizOffset, vertOffset + 32 * 7])}

      self.handlers = {
         'view': None,
         'memory': None,
         'eyesight': None,
         'smell': None,
         'save': None,
         'load': None,
         'time': None,
         'map': None}

   def render(self, screen):

      for label, entry in self.entries.items():
         entry.render(screen)

   def registerInputHandlers(self, input):

      def executeAction(entryId):
         handler = self.handlers[entryId]
         entry = self.entries[entryId]
         selectedValue = entry.toggleNextValue()
         handler(selectedValue)

      input.onKeyPressed(pygame.K_F1, lambda: executeAction('view'))
      input.onKeyPressed(pygame.K_F2, lambda: executeAction('memory'))
      input.onKeyPressed(pygame.K_F3, lambda: executeAction('eyesight'))
      input.onKeyPressed(pygame.K_F4, lambda: executeAction('smell'))
      input.onKeyPressed(pygame.K_F5, lambda: executeAction('save'))
      input.onKeyPressed(pygame.K_F6, lambda: executeAction('load'))
      input.onKeyPressed(pygame.K_F7, lambda: executeAction('time'))

   #
   # Event handlers
   #

   def onViewModeChanged(self, handler):
      self.handlers['view'] = handler

   def onMemoryModeChanged(self, handler):
      self.handlers['memory'] = handler

   def onEyesightChanged(self, handler):
      self.handlers['eyesight'] = handler

   def onSmellChanged(self, handler):
      self.handlers['smell'] = handler

   def onSave(self, handler):
      self.handlers['save'] = handler

   def onLoad(self, handler):
      self.handlers['load'] = handler

   def onTimeMultiplierChanged(self, handler):
      self.handlers['time'] = handler

   def onSetMap(self, handler):
      self.handlers['map'] = handler