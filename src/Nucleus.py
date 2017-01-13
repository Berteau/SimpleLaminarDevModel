from __future__ import division

from pylab import *
from random import *
from visual import *

class Nucleus: 
    def __init__(self, capacity, locationVector, layerColor, debug=False, silent=True):
        self.granular = False
        self.capacity = capacity
        self.cells = capacity
        self.outConnections = []
        self.outCount = 0
        self.inConnections = []
        self.openSlots = capacity
        self.locationVector = locationVector
        self.color = layerColor
        self.pruning = False
        self.pruneCount = 0
        self.height = int(5*self.capacity/100)
        self.silent = silent
        if not self.silent:
            self.rendering = box(pos=vector(locationVector[0],locationVector[1]+self.height/2,locationVector[2]), size=(21,self.height,21),color=self.color, opacity=0.3)
            self.fullRendering = box(pos=vector(self.locationVector[0],self.locationVector[1]+self.height*(self.cells / self.capacity)/2,self.locationVector[2]), size=(10.1,self.height*(self.cells / self.capacity),10.1),color=self.color, opacity=0.0)

    def update(self, t, debug=False):
        if debug: 
            print "Thalamic Update Called"
            print "Population:",self.cells,"/",self.capacity," \tOpenCells:", self.openSlots, "\tPrunecount:", self.pruneCount
        # Make sure outbound connections are in order
        self.outConnections = sorted(self.outConnections)
        # Try for level four outputs
        if self.outCount < self.cells:
            if debug: 
                print "outCount less than self.cells"
#            print "Thalamic Outputs: ", self.cells - self.outCount
            #for each output
            for o in range(len(self.outConnections)):
                # Assign number of cells equal to min(open, self.cells - self.outCount)
                numNewConnections = min(self.outConnections[o].getTargetFree(), self.cells - self.outCount)
                if numNewConnections > 0:
                    self.outCount += numNewConnections
                    if self.outConnections[o].multIncrement(numNewConnections):
                        if debug:
                            print "Added",numNewConnections," to connection", o
                    else:
                        if debug:
                            print "Failure!  This should not happen"
  
#        # Update Pruning
#        if self.capacity == self.cells and self.openSlots == 0 and self.pruning == False:
#                print "Thalamic Prune on!"
#                self.pruning = True
#                self.pruneCount = self.capacity / 3 # if full, prune 33% of connections over time.
#        if self.pruneCount > 0:
#            if sum([self.inConnections[i].number for i in range(len(self.inConnections))]) >= 1:
#                connToPrune = randint(0, len(self.inConnections)-1)
#                while self.inConnections[connToPrune].decrement() == False:
#                    connToPrune = randint(0, len(self.inConnections)-1)
                
        # Update rendering
        if not self.silent:
            if self.capacity == self.cells:
                self.rendering.opacity = 0.0
            if self.cells > 0:
                self.fullRendering.opacity = 1.0
            self.rendering.pos=vector(self.locationVector[0],self.locationVector[1]+self.height*(self.openSlots / self.capacity)/2,self.locationVector[2])
            self.rendering.size=(21,self.height*(self.openSlots / self.capacity),21)
            self.fullRendering.pos=vector(self.locationVector[0],self.locationVector[1]+self.height*(self.cells / self.capacity)/2,self.locationVector[2])
            self.fullRendering.size=(19,self.height*(self.cells / self.capacity),19)
        return True
