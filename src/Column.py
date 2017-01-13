from __future__ import division
from pylab import *
from pylab import *
from scipy import *
from random import *
from visual import *
from Layer import *

'''
Created on May 26, 2011

@author: stefan
'''

def gaussian(x, sigma, mu, scale):
        a = 1 / (sigma * sqrt(2*pi))
        b = mu
        c = sigma
        return int(scale*(a*exp(-(x-b)**2/(2*c**2))))

class Column: 
    def __init__(self, location, mean, variance, totalCells, time, outCount=100, inCount=10, debug=False, name="Placeholder", silent=True, timeDelay=40, pruningAmount=3):
        creationStart = mean - (2*variance)
        creationEnd = mean + (2*variance)
        self.qFunc = [gaussian(t, variance, mean, totalCells) for t in range(time)]
        self.silent = silent
        self.outCount=outCount
        self.inCount=inCount
        self.timeDelay=timeDelay
        self.pruningAmount = pruningAmount

        timeStep = int((creationEnd - creationStart)/6)
        layer1Cells = sum(self.qFunc[creationStart:creationStart+timeStep])
        layer6Cells = sum(self.qFunc[creationStart+timeStep:creationStart+2*timeStep])
        layer5Cells = sum(self.qFunc[creationStart+2*timeStep:creationStart+3*timeStep])
        layer4Cells = sum(self.qFunc[creationStart+3*timeStep:creationStart+4*timeStep])
        layer3Cells = sum(self.qFunc[creationStart+4*timeStep:creationStart+5*timeStep])
        layer2Cells = sum(self.qFunc[creationStart+5*timeStep:creationEnd])
        
        layer6 = Layer(self, layer6Cells, [location[0], 0, location[1]], color.red, silent=self.silent, layerNumber=6, inboundPerCell=self.inCount, outboundPerCell=self.outCount, timeDelay=self.timeDelay, pruningAmount=self.pruningAmount)
        layer5 = Layer(self, layer5Cells, [location[0], 0.1+layer6.height, location[1]], color.green, silent=self.silent, layerNumber=5, inboundPerCell=self.inCount, outboundPerCell=self.outCount, timeDelay=self.timeDelay, pruningAmount=self.pruningAmount)
        layer4 = Layer(self, layer4Cells, [location[0], 0.2+layer6.height+layer5.height, location[1]], color.blue, granular=True, silent=self.silent, layerNumber=4, inboundPerCell=self.inCount, outboundPerCell=self.outCount, timeDelay=self.timeDelay, pruningAmount=self.pruningAmount)
        layer3 = Layer(self, layer3Cells, [location[0], 0.3+layer6.height+layer5.height+layer4.height, location[1]], color.magenta, silent=self.silent, layerNumber=3, inboundPerCell=self.inCount, outboundPerCell=self.outCount, timeDelay=self.timeDelay, pruningAmount=self.pruningAmount)
        layer2 = Layer(self, layer2Cells, [location[0], 0.4+layer6.height+layer5.height+layer4.height+layer3.height, location[1]], color.yellow, silent=self.silent, layerNumber=2, inboundPerCell=self.inCount, outboundPerCell=self.outCount, timeDelay=self.timeDelay, pruningAmount=self.pruningAmount)
        layer1 = Layer(self, layer1Cells, [location[0], 0.5+layer6.height+layer5.height+layer4.height+layer3.height+layer2.height, location[1]], color.cyan, granular=True, silent=self.silent, layerNumber=1, inboundPerCell=self.inCount, outboundPerCell=self.outCount, timeDelay=self.timeDelay, pruningAmount=self.pruningAmount)
        
        self.layers = [layer6, layer5, layer4, layer3, layer2, layer1]
        self.location = location
        self.debug = debug
        self.name = name
        
        if debug:
            print "CreationStart:", creationStart
            print "CreationEnd:", creationEnd
            print "Total cells within creation period:", sum(self.qFunc[creationStart:creationEnd])
            for l in range(len(self.layers)):
                layer = self.layers[l]
                print "Layer",l,"\tPopulation:",layer.cells,"/",layer.capacity," \tOpenCells:", layer.openSlots, "\tPrunecount:", layer.pruneCount
        
    def update(self, t):   
        layerNumbers = [4,3,2,1,0,5]     
        for c in range(int(self.qFunc[t])):
            # Add to the next layer that is open
            i=5
            while self.layers[layerNumbers[i]].addCell() == False:
#                print i
                if i > 0:
                    i -= 1
                else:
#                    print "Cell discarded - All layers full."
                    break
        for l in layerNumbers:
            layer = self.layers[l]
            layer.update()

    def openSlots(self):
        layerNames = [6, 5, 4, 3, 2, 1]
        for l in range(len(self.layers)):
            layer = self.layers[l]
            print "Layer", layerNames[l] 
            print "\tOpen Cells:", layer.openSlots
            print "\tOut Count:", layer.outCount
            print "\tPopulation:", layer.cells
            
    def sortYourConnections(self):
        for l in self.layers:
            l.sortConnections()