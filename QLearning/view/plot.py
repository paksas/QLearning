import matplotlib.pyplot as plt
import numpy as np

class Plot:

   def __init__(self):

      self.axes = plt.gca()
      self.axes.set_xlim(0, 100)
      self.axes.set_ylim(0, 40)
      
      self.nextIdx = 0
      self.xdata = []
      self.ydata = []
      self.medianYdata = []

      self.samplesLine, = self.axes.plot(self.xdata, self.ydata, 'r-')
      self.medianLine, = self.axes.plot(self.xdata, self.medianYdata, 'b-')

      plt.ion() # enable interactive plotting

   def show(self):
      plt.draw()
      plt.pause(0.05)

   def resetPlot(self):

      self.nextIdx = 0
      self.xdata = []
      self.ydata = []
      self.medianYdata = []

      self.samplesLine.set_xdata(self.xdata)
      self.samplesLine.set_ydata(self.ydata)

      self.medianLine.set_xdata(self.xdata)
      self.medianLine.set_ydata(self.medianYdata)

      plt.draw()
      plt.pause(0.05)

   def __calcVertRange__(self):
      vertRange = self.medianYdata[len(self.medianYdata) - 1] * 2
      return vertRange

   def addSample(self, val):

      if (self.nextIdx >= 100):
         self.axes.set_ylim(0, self.__calcVertRange__())
         self.resetPlot()

      self.xdata.append(self.nextIdx)
      self.nextIdx += 1

      self.ydata.append(val)

      medianVal = np.median(self.ydata)
      self.medianYdata.append(medianVal)

      self.samplesLine.set_xdata(self.xdata)
      self.samplesLine.set_ydata(self.ydata)

      self.medianLine.set_xdata(self.xdata)
      self.medianLine.set_ydata(self.medianYdata)

      plt.draw()
      plt.pause(0.05)

