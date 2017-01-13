from __future__ import division

from pylab import *
from math import *
from visual import *

def findAxis(source, target):
    return [target.locationVector[dimension] - source.locationVector[dimension] for dimension in range(len(source.locationVector))]
    
class Connection:
    def __init__(self, sourceLayer, targetLayer, opacity, targetLayerNumber, targetColumnNumber, debug=False, silent=True):
        self.source = sourceLayer
        self.target = targetLayer
        self.number = 0
        self.opacity = opacity
        self.targetLayerNumber = targetLayerNumber
        self.targetColumnNumber = targetColumnNumber
        self.silent = silent
        # Define distance
        x1 = self.source.locationVector[0]
        y1 = self.source.locationVector[1]
        z1 = self.source.locationVector[2]
        x2 = self.source.locationVector[0]
        y2 = self.source.locationVector[1]
        z2 = self.source.locationVector[2]
#        self.distance = sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
        self.distance = sqrt((x1 - x2)**2 + (z1 - z2)**2)
        self.source.outConnections.append(self)
        self.target.inConnections.append(self)
        if not self.silent:
            self.rendering = cylinder(pos=self.source.locationVector, axis=findAxis(self.source, self.target), radius=0, color=color.white, opacity=self.opacity)
        self.debug = debug
        
    def __lt__(self, other, epsilon=0.000001):
        if other.distance == self.distance:
            if other.targetLayerNumber > self.targetLayerNumber:
                return other
            else:
                return self
        if other.distance < self.distance:
            return other
        else:
            return self
    
    def increment(self):
        if self.debug:
            print "Debug: connection incremented!  Current count before increment: ", self.number
        if self.target.openSlots > 0:
            self.number += 1
            self.target.openSlots -= 1
            if not self.silent:
                self.rendering.radius += 0.005
            return True
        else:
            return False
        
    def multIncrement(self, n):
        if self.target.openSlots >= n:
            self.number += n
            self.target.openSlots -= n
            if not self.silent:
                self.rendering.radius += (0.005*n)
            return True
        else:
            return False
    
    def decrement(self):
        if self.number >= 1:
            self.number -=1
            self.target.openSlots += 1
            if not self.silent:
                self.rendering.radius -= 0.005
            return True
        else:
            return False
    
    def getTargetFree(self):
        return self.target.openSlots
    