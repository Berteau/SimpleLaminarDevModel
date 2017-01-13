from __future__ import division
from pylab import *
from scipy import *
from random import *
from visual import *
from Layer import *
from Column import *
from Nucleus import *
from Connection import *

time = 160
activeTimeStart = 0
activeTimeEnd = 0

sum1 = 250
sum2 = 450
outCount = 110
inCount = 80

def gaussian(x, sigma, mu, scale):
        a = 1 / (sigma * sqrt(2*pi))
        b = mu
        c = sigma
        return int(scale*(a*exp(-(x-b)**2/(2*c**2))))

mean1 = 25
mean2 = 35
var1 = 8
var2 = 16

q1 = [gaussian(t, var1, mean1, sum1) for t in range(time)]
q2 = [gaussian(t, var2, mean2, sum2) for t in range(time)]

#figure()
#plot(q1)
#plot(q2)
#show()

c1 = Column([-30, -10], mean1, var1, sum1, time, debug=False, silent=False, name="c1")
c2 = Column([-30, 10], mean1, var1, sum1, time, debug=False, silent=False, name="c2")
c3 = Column([30, -10], mean2, var2, sum2, time, debug=False, silent=False, name="c3")
c4 = Column([30, 10], mean2, var2, sum2, time, debug=False, silent=False, name="c4")
thalamus = Nucleus(400, [0, -30, 0], color.white, silent=False)
columns = [c1, c2, c3, c4]

for c in range(4):
    column = columns[c]
    for tc in range(4):
        if tc != c:
            targetColumn = columns[tc]
            for sl in range(len(column.layers)):
                sourceLayer = column.layers[sl]
                for tl in range(len(targetColumn.layers)):
                    targetLayer = targetColumn.layers[tl]
#                    print "Connecting column", c,"layer",sl, "to column", tc,"layer",tl
                    if c > 1:
                        Connection(sourceLayer, targetLayer, 0.0, tl, tc, silent=False)
                    else:
                        Connection(sourceLayer, targetLayer, 1.0, tl, tc, silent=False)

# Possible connections from layer VI to Thalamus
Connection(c1.layers[0], thalamus, 1.0, -1, -1, silent=False, debug=True)
Connection(c2.layers[0], thalamus, 1.0, -1, -1, silent=False, debug=True)
Connection(c3.layers[0], thalamus, 1.0, -1, -1, silent=False, debug=True)
Connection(c4.layers[0], thalamus, 1.0, -1, -1, silent=False, debug=True)

# Possible Connections from layer V to Thalamus
Connection(c1.layers[1], thalamus, 1.0, -1, -1, silent=False, debug=True)
Connection(c2.layers[1], thalamus, 1.0, -1, -1, silent=False, debug=True)
Connection(c3.layers[1], thalamus, 1.0, -1, -1, silent=False, debug=True)
Connection(c4.layers[1], thalamus, 1.0, -1, -1, silent=False, debug=True)

# Possible Connections from layer III to Thalamus
Connection(c1.layers[3], thalamus, 1.0, -1, -1, silent=False, debug=True)
Connection(c2.layers[3], thalamus, 1.0, -1, -1, silent=False, debug=True)
Connection(c3.layers[3], thalamus, 1.0, -1, -1, silent=False, debug=True)
Connection(c4.layers[3], thalamus, 1.0, -1, -1, silent=False, debug=True)

# Possible Connections from layer II to Thalamus
Connection(c1.layers[4], thalamus, 1.0, -1, -1, silent=False, debug=True)
Connection(c2.layers[4], thalamus, 1.0, -1, -1, silent=False, debug=True)
Connection(c3.layers[4], thalamus, 1.0, -1, -1, silent=False, debug=True)
Connection(c4.layers[4], thalamus, 1.0, -1, -1, silent=False, debug=True)

Connection(thalamus, c1.layers[2], 1.0, 2, 1, silent=False)
Connection(thalamus, c2.layers[2], 1.0, 2, 1, silent=False)
Connection(thalamus, c3.layers[2], 1.0, 2, 1, silent=False)
Connection(thalamus, c4.layers[2], 1.0, 2, 1, silent=False)

c1.sortYourConnections()
c2.sortYourConnections()
c3.sortYourConnections()
c4.sortYourConnections()

for t in range(time): # For each time step
    rate(10)
    toUpdate = [c1, c2, c3, c4, thalamus]
    random.shuffle(toUpdate)
#    print toUpdate
    for structure in toUpdate:
        structure.update(t)

interConnections = ones([4, 4, 6, 6]) * -1
columnToThal = ones([4,6]) * -1
euToDys = zeros([6,6])
dysToEu = zeros([6,6])

for sourceColumnNumber in range(4):
    column = columns[sourceColumnNumber]
    for targetColumnNumber in range(4):
        targetColumn = columns[targetColumnNumber]
#        print targetColumn.name
        for sourceLayerNumber in range(6):
            for connectionNumber in range(len(column.layers[sourceLayerNumber].outConnections)):
#                print "Target Column:", column.layers[sourceLayerNumber].outConnections[connectionNumber].targetColumnNumber, ":", targetColumnNumber
                if column.layers[sourceLayerNumber].outConnections[connectionNumber].targetColumnNumber == targetColumnNumber:
                    if column.layers[sourceLayerNumber].outConnections[connectionNumber].targetLayerNumber == -1:
                        columnToThal[sourceColumnNumber, sourceLayerNumber] = column.layers[sourceLayerNumber].outConnections[connectionNumber].number
                    else:
                        interConnections[sourceColumnNumber, targetColumnNumber, sourceLayerNumber, column.layers[sourceLayerNumber].outConnections[connectionNumber].targetLayerNumber] = column.layers[sourceLayerNumber].outConnections[connectionNumber].number

euToDysTotal = sum(sum(sum(interConnections[[2,3],0:2,:,:])))
euHighToDysLow = sum(sum(sum(interConnections[[2,3],0:2,4:6,0:2])))
euLowToDysHigh = sum(sum(sum(interConnections[[2,3],0:2,0:2,4:6])))

dysToEuTotal = sum(sum(sum(interConnections[[0,1],2:4,:,:])))
dysLowToEuHigh = sum(sum(sum(interConnections[[0,1],2:4,0:2,4:6])))
dysHighToEuLow = sum(sum(sum(interConnections[[0,1],2:4,4:6,0:2])))

print "Results\n~~~~~~~~~~~~~~~~~~~~~~~"
print "Eulaminate to Dyslaminate Total:", euToDysTotal
print "Eulaminate high to Dyslaminate low:", euHighToDysLow
print "Eulaminate low to Dyslaminate high:", euLowToDysHigh
print "Percent Total:", (euHighToDysLow / euToDysTotal)*100
print "Percent of inclined projections:", (euHighToDysLow / (euHighToDysLow+euLowToDysHigh))*100

print "\nDyslaminate to Eulaminate Total:", dysToEuTotal
print "Dyslaminate low to Eulaminate high:", dysLowToEuHigh
print "Dyslaminate high to Eulaminate low:", dysHighToEuLow
print "Percent:", (dysLowToEuHigh / dysToEuTotal)*100
print "Percent of inclined projections:", (dysHighToEuLow / (dysHighToEuLow+dysLowToEuHigh))*100
