#31/10/2018 
#This is the main file where most stuff is done. Classes will be written as their own modules yeah. 
import matplotlib.pyplot as plt
import scipy.ndimage.filters
import math
import numpy as np

import tripyr
import cuboid
import sphere
import addDeformation as aD
#import sys

#Set of functions
#Function to add noise to the matrix
def addPoissonNoise(Matrix):
    for i in range(len(xRange)):
        for u in range (len(yRange)):
            noise = np.random.poisson(5)            #How big should the noise be? Any ideas? #relative to mean intensity
            Matrix[i][u] += noise
            
def calcThicknessMatrix(objects,xProbeRange,yProbeRange):
    thicknessMatrix = np.zeros((len(xProbeRange),len(yProbeRange)))
    for i in range(len(xProbeRange)):
        for u in range (len(yProbeRange)):
            #Random probability for the object to rotate during imaging, by a small angle.
            rotRand = np.random.randint(0,2)
            if rotRand == 1:
                alphaRand = np.random.randint(0,3)
                betaRand = np.random.randint(0,3)
                gammaRand = np.random.randint(0,3)
    
            for a in range(len(objects)):
                thisObject = objects[a]
                
                if rotRand == 1:
                    thisObject.alpha += alphaRand
                    thisObject.beta += betaRand
                    thisObject.gamma += gammaRand
                
                intersects = thisObject.findIntersectionThickness(thisObject.planes,i,u)
                if intersects:
                    if not thisObject.deformation:
                        thicknessMatrix[i][u] += intersects                              #Outputs the intersects on thickness matrix!
                    else:
                        thicknessMatrix[i][u] -= intersects
        # print(thicknessMatrix[50][50])

    return thicknessMatrix

xRange = [i for i in range(0,100)]        #100x100 scan for probe, across 100x100
yRange = [i for i in range(0,100)]
zRange = [i for i in range(0,100)]


#Generating an test object, let a cube.

cLMax = 50     #Cube length max

#Generate random parameters of the cube
aRand = np.random.randint(40,50)
bRand = np.random.randint(40,50)
cRand = np.random.randint(40,50)

#Generate random numbers for start position
xPosRandom = np.random.randint(45,56)         #This is to make sure the object stays within the confides of the image!
yPosRandom = np.random.randint(45,56)          #Centered at between 45 and 55.


rRand = np.random.randint(cLMax/10,cLMax/5)
#sphere = sphere.sphere("xs",False,0,0,0,xPosRandom,yPosRandom,cLMax,xRange,yRange,rRand)

#sphere.calcThicknessMatrix()

alphaRand = np.random.randint(0,90)
betaRand = np.random.randint(0,90)
gammaRand = np.random.randint(0,90)

#Random cuboid object
#cube = object.cuboid("cmj",0,0,0,xPosRandom,yPosRandom,cLMax,xRange,yRange,aRand,bRand,cRand)
#cube = object.cuboid("cmj",alphaRand,betaRand,gammaRand,xPosRandom,yPosRandom,50,xRange,yRange,aRand,bRand,cRand)

cube = cuboid.cuboid("cmj",False,alphaRand,betaRand,gammaRand,xPosRandom,yPosRandom,50,xRange,yRange,50,50,50)
objects = [cube]

deforms = aD.addDeformation(cube,'cuboid')
dA = deforms.deformArray


for i in range(len(dA)):
    deformation = tripyr.tripyr("xcl",True,alphaRand,betaRand,gammaRand,xPosRandom,yPosRandom,50,xRange,yRange,dA[i][0],dA[i][1],dA[i][2],dA[i][3],cube.xAxis,cube.yAxis,cube.zAxis)
    objects.append(deformation)


for i in range(len(objects)):
    objects[i].doRotation()

image = calcThicknessMatrix(objects,xRange,yRange) + 10

#Adding gaussian blur
image = scipy.ndimage.filters.gaussian_filter(image,1)

#Adding poisson noise
addPoissonNoise(image)
           
plt.pcolormesh(xRange, yRange, image, cmap="Greys_r")
plt.show()
#plt.savefig('SimulationImages/Spheres/plot'+str(sys.argv[1])+'.png')     #sys.argv is the input from the bash script
#plt.savefig('Cuboids/plot'+str(200)+'.png')     #sys.argv is the input from the bash script

