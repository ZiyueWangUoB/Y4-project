#31/10/2018 
#This is the main file where most stuff is done. Classes will be written as their own modules yeah. 
import matplotlib.pyplot as plt
import numpy as np

import object


#Probe params
xRange = [i for i in range(0,1000)]        #100x100 scan for probe, across 100x100
yRange = [i for i in range(0,1000)]

#Generating an test object, let a cube.

cLMax = 500     #Cube length max

#Generate random parameters of the cube
aRand = np.random.randint(0,cLMax)
bRand = np.random.randint(0,cLMax)
cRand = np.random.randint(0,cLMax)

#Generate random numbers for start position
xPosRandom = np.random.randint(cLMax/2,max(xRange)-cLMax/2)
yPosRandom = np.random.randint(cLMax/2,max(yRange)-cLMax/2)

#cube = object.cuboid("tungsten",0,0,0,xPosRandom,yPosRandom,xRange,yRange,aRand,bRand,cRand)

#cube.calcThickness()
#print(cube.thicknessMatrix)

rRand = np.random.randint(0,cLMax)
sphere = object.sphere("xs",0,0,0,xPosRandom,yPosRandom,xRange,yRange,rRand)
print(rRand)

sphere.calcThicknessMatrix()



#plotting of STEM prototype (no noise yet)

A = sphere.thicknessMatrix

def addPoissonNoise(Matrix):
    for i in range(len(xRange)):
        for u in range (len(yRange)):
            noise = np.random.poisson(rRand)            #How big should the noise be? Any ideas?
            Matrix[i][u] += noise

addPoissonNoise(A)            
            
plt.pcolormesh(xRange, yRange, A, cmap="Greys_r")
plt.show()


