from __future__ import division

from pylab import *
from random import *
from visual import *
from collections import deque

class Layer: 
    def __init__(self, column, capacity, locationVector, layerColor, granular=False, timeDelay=40, silent=True, inboundPerCell=10, outboundPerCell=20, layerNumber=99, pruningAmount=3):
        self.column = column
        self.granular = granular
        self.capacity = capacity
        self.cells = 0
        self.matureCellsLastCount = 0
        self.historicalCells = deque()
        for i in range(timeDelay):
            self.historicalCells.appendleft(0)   
        self.outConnections = []
        self.outCount = 0
        self.inConnections = []
        self.openSlots = 0
        self.locationVector = locationVector
        self.color = layerColor
        self.pruning = False
        self.pruneCount = 0
        self.pruningAmount = pruningAmount
        self.height = int(self.capacity/6)
        self.silent = silent
        self.layerNumber = layerNumber
        self.inboundPerCell = inboundPerCell
        self.outboundPerCell = outboundPerCell
        self.timeDelay = timeDelay
        if not self.silent:
            self.rendering = box(pos=vector(locationVector[0],locationVector[1]+self.height/2,locationVector[2]), size=(11,self.height,11),color=self.color, opacity=0.3)
            self.fullRendering = box(pos=vector(self.locationVector[0],self.locationVector[1]+self.height*(self.cells / self.capacity)/2,self.locationVector[2]), size=(10.1,self.height*(self.cells / self.capacity),10.1),color=self.color, opacity=0.0)

    def sortConnections(self):
        # Make sure outbound connections are in order
            self.outConnections = sorted(self.outConnections)

    def addCell(self):
        # Do we have enough cells
        if (self.capacity - self.cells) > 0:
            self.cells += 1
            if self.layerNumber in [2,3,5,6]:
                self.openSlots += self.inboundPerCell #/ 3
            else:
                self.openSlots += self.inboundPerCell
        else:
            return False

    def update(self):
        # Add a new count to the queue
        self.historicalCells.appendleft(self.cells)   

        # Figure out how many cells are old enough to make connections
        matureCells = self.historicalCells.pop()
        newlyMatureCells = matureCells - self.matureCellsLastCount
        self.matureCellsLastCount = matureCells
        
#        # If the layer is in 2, 3, 5, or 6, and therefore has pyramidal cells
#        # Add apical dendrite connections
#        if self.layerNumber in [2,3,5,6]:
#            newApicalSlotCount = (2 * newlyMatureCells * self.inboundPerCell) / 3
#            apicalTerminationIndex = min((6 - self.layerNumber) + 4, 5) # Travel up 4 layers, maxing out at layer 1 
#            self.column.layers[apicalTerminationIndex].openSlots += newApicalSlotCount            
        
        # If the layer is not granular, and therefore makes outbound connections, Take any free cells and connect
        if not self.granular:
            # Do we have any free mature cells?
            if self.outCount < matureCells * self.outboundPerCell:
                desiredConnections = (matureCells * self.outboundPerCell) - self.outCount
                #for each output
                for o in range(len(self.outConnections)):
                    # Assign number of cells equal to min(open, self.cells - self.outCount)
                    numNewConnections = min(self.outConnections[o].getTargetFree(), desiredConnections)
                    if numNewConnections > 0:
                        self.outConnections[o].multIncrement(numNewConnections)
                        self.outCount += numNewConnections
                        desiredConnections -= numNewConnections
                        
        # Update Pruning
        if self.capacity == self.cells and self.openSlots == 0 and self.pruning == False:
#                print "Prune on!"
                self.pruning = True
                self.pruneCount = self.capacity / self.pruningAmount # if full, prune 33% of connections over time.
        if self.pruneCount > 0:
            cellsToPrune = min(self.capacity / (self.pruningAmount*4), sum([self.inConnections[i].number for i in range(len(self.inConnections))]))
            if sum([self.inConnections[i].number for i in range(len(self.inConnections))]) >= cellsToPrune:
                self.pruneCount -= cellsToPrune
                while cellsToPrune > 0:
                    connToPrune = randint(0, len(self.inConnections)-1)
                    while self.inConnections[connToPrune].decrement() == False:
                        connToPrune = randint(0, len(self.inConnections)-1)
                    cellsToPrune -= 1
            
        if not self.silent:        
            # Update rendering
            if self.capacity == self.cells:
                self.rendering.opacity = 0.0
            if self.cells > 0:
                self.fullRendering.opacity = 1.0
            self.rendering.pos=vector(self.locationVector[0],self.locationVector[1]+self.height*(self.openSlots / self.capacity)/2,self.locationVector[2])
            self.rendering.size=(11,self.height*(self.openSlots / self.capacity),11)
            self.fullRendering.pos=vector(self.locationVector[0],self.locationVector[1]+self.height*(self.cells / self.capacity)/2,self.locationVector[2])
            self.fullRendering.size=(8,self.height*(self.cells / self.capacity),8)
        return True